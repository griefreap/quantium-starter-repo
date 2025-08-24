# app.py
# Dash app for Pink Morsel Sales — production-ready & test-friendly

import os
import pandas as pd
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output, no_update

# ---------- Data loading ----------
DATA_FILE = "cleaned_sales.csv"
PRICE_CHANGE_DATE = pd.Timestamp("2021-01-15")

def load_data(path: str) -> pd.DataFrame:
    if not os.path.exists(path):
        # Create an empty frame with the expected columns so the app still loads
        return pd.DataFrame(columns=["Sales", "Date", "Region"])
    df = pd.read_csv(path)
    # Normalize columns
    df.columns = [c.strip().title() for c in df.columns]
    # Parse types
    if "Date" in df.columns:
        df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    if "Sales" in df.columns:
        df["Sales"] = pd.to_numeric(df["Sales"], errors="coerce")
    # Keep only rows that have the essentials
    df = df.dropna(subset=["Date", "Sales", "Region"])
    # Normalize region capitalization to match RadioItems values
    df["Region"] = df["Region"].str.title()
    return df

df = load_data(DATA_FILE)

# ---------- App ----------
app = Dash(__name__, suppress_callback_exceptions=True)
server = app.server  # for deployment (gunicorn, etc.)

# Global styles
APP_BG = "#f7fbff"
HEADER_BG = "#e8f3f8"           # soft teal block behind heading
HEADER_TEXT = "#0c5a6b"         # teal blue
GRID_COLOR = "#e6ecf5"
FONT_FAMILY = "Inter, Segoe UI, Arial, sans-serif"

app.layout = html.Div(
    style={"backgroundColor": APP_BG, "minHeight": "100vh", "padding": "24px"},
    children=[
        # ---- Header (ID required by tests) ----
        html.Div(
            id="header",
            children=html.H1(
                "Pink Morsel Sales Dashboard",
                style={
                    "margin": 0,
                    "fontWeight": 800,
                    "letterSpacing": "0.2px",
                    "fontFamily": FONT_FAMILY,
                },
            ),
            style={
                "backgroundColor": HEADER_BG,
                "color": HEADER_TEXT,
                "padding": "18px 22px",
                "borderRadius": "14px",
                "textAlign": "center",
                "boxShadow": "0 4px 14px rgba(12,90,107,0.08)",
                "marginBottom": "18px",
            },
        ),

        # ---- Controls ----
        html.Div(
            style={
                "backgroundColor": "white",
                "borderRadius": "14px",
                "padding": "16px 18px",
                "boxShadow": "0 2px 10px rgba(16,24,40,0.06)",
                "marginBottom": "16px",
            },
            children=[
                html.Label(
                    "Select Region:",
                    style={
                        "display": "block",
                        "fontWeight": 600,
                        "marginBottom": "8px",
                        "fontFamily": FONT_FAMILY,
                        "color": "#0f172a",
                    },
                ),
                dcc.RadioItems(
                    id="region-picker",  # <- required by tests
                    options=[
                        {"label": "All", "value": "All"},
                        {"label": "East", "value": "East"},
                        {"label": "North", "value": "North"},
                        {"label": "South", "value": "South"},
                        {"label": "West", "value": "West"},
                    ],
                    value="All",
                    inline=True,
                    inputStyle={"marginRight": "6px"},
                    labelStyle={
                        "marginRight": "18px",
                        "fontFamily": FONT_FAMILY,
                        "cursor": "pointer",
                    },
                ),
            ],
        ),

        # ---- Graph (ID required by tests) ----
        html.Div(
            style={
                "backgroundColor": "white",
                "borderRadius": "14px",
                "padding": "10px 14px 6px 14px",
                "boxShadow": "0 2px 10px rgba(16,24,40,0.06)",
                # fill remaining space elegantly on most screens
                "height": "78vh",
            },
            children=[
                dcc.Graph(
                    id="sales-graph",
                    style={"height": "100%"},
                    config={"displayModeBar": True, "responsive": True},
                )
            ],
        ),
    ],
)

# ---------- Figure builder ----------
def build_figure(region: str) -> go.Figure:
    # If no data, show a graceful placeholder
    if df.empty:
        fig = go.Figure()
        fig.update_layout(
            template="plotly_white",
            paper_bgcolor="white",
            plot_bgcolor="white",
            margin=dict(l=40, r=20, t=20, b=40),
            xaxis_title="Date",
            yaxis_title="Sales",
            font=dict(family=FONT_FAMILY, size=14),
        )
        fig.add_annotation(
            x=0.5,
            y=0.5,
            xref="paper",
            yref="paper",
            text="No data available",
            showarrow=False,
            font=dict(size=16, color="#64748b"),
        )
        return fig

    # Filter
    data = df if region == "All" else df[df["Region"] == region]

    if data.empty:
        # Same placeholder if filter eliminates all rows
        return build_figure("All")

    # Aggregate to daily totals for a clean single line
    daily = (
        data.groupby("Date", as_index=False)["Sales"]
        .sum()
        .sort_values("Date")
        .reset_index(drop=True)
    )

    # Main line
    fig = go.Figure(
        data=[
            go.Scatter(
                x=daily["Date"],
                y=daily["Sales"],
                mode="lines",
                line=dict(width=3),
                name="Sales",
                hovertemplate="<b>%{x|%b %d, %Y}</b><br>Sales: %{y:.0f}<extra></extra>",
            )
        ]
    )

    # Price-change vertical line + annotation
    fig.add_vline(
        x=PRICE_CHANGE_DATE,
        line_dash="dash",
        line_color="#0c5a6b",
        line_width=2,
        opacity=0.8,
    )
    fig.add_annotation(
        x=PRICE_CHANGE_DATE,
        y=1.02,
        xref="x",
        yref="paper",
        showarrow=False,
        text="Price change (2021-01-15)",
        font=dict(color="#0c5a6b", size=12),
        bgcolor="#e8f3f8",
        bordercolor="#0c5a6b",
        borderwidth=1,
        borderpad=4,
    )

    # Layout polish
    fig.update_layout(
        template="plotly_white",
        paper_bgcolor="white",
        plot_bgcolor="white",
        margin=dict(l=50, r=30, t=10, b=60),
        hovermode="x unified",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0),
        xaxis=dict(
            title="Date",
            gridcolor=GRID_COLOR,
            showspikes=True,
            spikethickness=1,
            spikedash="dot",
            spikesnap="cursor",
            spikemode="across",
            rangeselector=dict(
                buttons=list(
                    [
                        dict(count=6, label="6m", step="month", stepmode="backward"),
                        dict(count=1, label="1y", step="year", stepmode="backward"),
                        dict(step="all"),
                    ]
                )
            ),
            rangeslider=dict(visible=True),
        ),
        yaxis=dict(title="Sales", gridcolor=GRID_COLOR, zeroline=False),
        font=dict(family=FONT_FAMILY, size=14, color="#0f172a"),
    )

    return fig

# ---------- Callbacks ----------
@app.callback(Output("sales-graph", "figure"), Input("region-picker", "value"))
def update_figure(selected_region):
    try:
        return build_figure(selected_region or "All")
    except Exception:
        # Fail safe: keep the existing figure if anything unexpected happens
        return no_update


# ---------- Run (only when executed directly) ----------
if __name__ == "__main__":
    # Do NOT enable debug=True in CI to keep logs clean & avoid reloader issues
    app.run(host="127.0.0.1", port=8050, debug=False)

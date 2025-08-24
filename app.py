import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output


# load data
df = pd.read_csv("cleaned_sales.csv")
df["Date"] = pd.to_datetime(df["Date"])
df["Region"] = df["Region"].astype(str).str.lower()

app = Dash(__name__)
app.title = "Pink Morsel Sales Visualiser"

PRICE_INCREASE = pd.Timestamp("2021-01-15")

page_style = {
    "fontFamily": "Arial, sans-serif",
    "background": "#f8f9fa",
    "padding": "24px",
}

card_style = {
    "maxWidth": "1000px",
    "margin": "0 auto",
    "background": "#ffffff",
    "padding": "20px",
    "borderRadius": "10px",
    "boxShadow": "0 4px 10px rgba(0,0,0,0.08)",
}

app.layout = html.Div(
    style=page_style,
    children=[
        html.H1(
            "Soul Foods · Pink Morsel Sales",
            style={"textAlign": "center", "marginBottom": "10px"},
        ),
        html.P(
            "Use the region selector to focus the chart. "
            "Dashed line marks the 2021-01-15 price increase.",
            style={"textAlign": "center", "marginBottom": "20px"},
        ),
        html.Div(
            style={"textAlign": "center", "marginBottom": "16px"},
            children=[
                html.Label(
                    "Region:",
                    style={"fontWeight": "bold", "marginRight": "12px"},
                ),
                dcc.RadioItems(
                    id="region",
                    options=[
                        {"label": "All", "value": "all"},
                        {"label": "North", "value": "north"},
                        {"label": "East", "value": "east"},
                        {"label": "South", "value": "south"},
                        {"label": "West", "value": "west"},
                    ],
                    value="all",
                    labelStyle={
                        "display": "inline-block",
                        "marginRight": "16px",
                        "cursor": "pointer",
                    },
                    inputStyle={"marginRight": "6px"},
                ),
            ],
        ),
        html.Div(
            style=card_style,
            children=[dcc.Graph(id="sales-line")],
        ),
    ],
)


@app.callback(Output("sales-line", "figure"), Input("region", "value"))
def update_chart(region_value: str):
    if region_value == "all":
        dff = df.copy()
        title_suffix = "All Regions"
    else:
        dff = df[df["Region"] == region_value]
        title_suffix = region_value.capitalize()

    # aggregate by date
    series = (
        dff.groupby("Date", as_index=False)["Sales"]
        .sum()
        .sort_values("Date")
    )

    fig = px.line(
        series,
        x="Date",
        y="Sales",
        labels={"Date": "Date", "Sales": "Total Sales ($)"},
        title=f"Pink Morsel Sales Over Time · {title_suffix}",
        template="plotly_white",
    )

    # price increase marker
    ymax = series["Sales"].max() if not series.empty else 0
    fig.add_vline(
        x=PRICE_INCREASE, line_width=2, line_dash="dash", line_color="crimson"
    )
    fig.add_annotation(
        x=PRICE_INCREASE,
        y=ymax,
        text="Price Increase (2021-01-15)",
        showarrow=True,
        arrowhead=2,
        ax=0,
        ay=-40,
        bgcolor="rgba(255,255,255,0.7)",
        bordercolor="crimson",
    )

    fig.update_layout(margin=dict(l=40, r=40, t=60, b=40))
    return fig


if __name__ == "__main__":
    app.run(debug=True)

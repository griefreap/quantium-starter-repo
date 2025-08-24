import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go

# =======================
# Load and prepare data
# =======================
data = pd.read_csv("cleaned_sales.csv")
data["Date"] = pd.to_datetime(data["Date"])

regions = ["All"] + sorted(data["Region"].unique())

# =======================
# Initialize Dash app
# =======================
app = dash.Dash(__name__)
app.title = "Pink Morsel Sales Dashboard"
server = app.server

# =======================
# App Layout
# =======================
app.layout = html.Div(
    [
        html.H1(
            "Soul Foods · Pink Morsel Sales",
            style={"textAlign": "center", "marginBottom": "10px"},
            id="header",  # <-- ID added for testing
        ),
        html.P(
            "Visualizing sales before and after the 2021-01-15 price increase.",
            style={"textAlign": "center"},
        ),
        html.Div(
            [
                html.Label("Filter by Region:", style={"fontWeight": "bold"}),
                dcc.RadioItems(
                    id="region-picker",  # <-- ID added for testing
                    options=[{"label": r, "value": r} for r in regions],
                    value="All",
                    labelStyle={"display": "inline-block", "marginRight": "10px"},
                ),
            ],
            style={
                "border": "1px solid #ddd",
                "padding": "10px",
                "marginBottom": "20px",
                "borderRadius": "5px",
            },
        ),
        dcc.Graph(id="sales-graph"),  # <-- ID added for testing
    ],
    style={"maxWidth": "1000px", "margin": "auto"},
)


# =======================
# Callback for interactivity
# =======================
@app.callback(
    Output("sales-graph", "figure"),
    Input("region-picker", "value"),
)
def update_graph(selected_region):
    if selected_region == "All":
        filtered = data
        title_region = "All Regions"
    else:
        filtered = data[data["Region"] == selected_region]
        title_region = selected_region

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=filtered["Date"],
            y=filtered["Sales"],
            mode="lines",
            name="Sales",
            line=dict(color="blue"),
        )
    )

    fig.add_vline(
        x=pd.Timestamp("2021-01-15"),
        line=dict(color="red", dash="dash"),
        annotation_text="Price Increase (2021-01-15)",
        annotation_position="top right",
    )

    fig.update_layout(
        title=f"Pink Morsel Sales Over Time · {title_region}",
        xaxis_title="Date",
        yaxis_title="Total Sales ($)",
        template="plotly_white",
    )

    return fig


# =======================
# Run app
# =======================
if __name__ == "__main__":
    app.run(debug=True)

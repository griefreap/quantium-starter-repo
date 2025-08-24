import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output

# Load the data
df = pd.read_csv("cleaned_sales.csv")
df["Date"] = pd.to_datetime(df["Date"])

# Create the app
app = Dash(__name__)

app.layout = html.Div(
    style={"fontFamily": "Arial", "margin": "40px"},
    children=[
        html.H1(
            "Pink Morsel Sales Visualizer",
            style={"textAlign": "center", "color": "#FF69B4"},
        ),
        html.Label(
            "Filter by Region:",
            style={"fontWeight": "bold", "marginTop": "20px"},
        ),
        dcc.RadioItems(
            id="region-filter",
            options=[
                {"label": "North", "value": "north"},
                {"label": "East", "value": "east"},
                {"label": "South", "value": "south"},
                {"label": "West", "value": "west"},
                {"label": "All", "value": "all"},
            ],
            value="all",
            labelStyle={"display": "inline-block", "marginRight": "20px"},
        ),
        dcc.Graph(id="sales-graph"),
    ],
)


@app.callback(Output("sales-graph", "figure"), Input("region-filter", "value"))
def update_graph(selected_region):
    if selected_region == "all":
        filtered_df = df
    else:
        filtered_df = df[df["Region"].str.lower() == selected_region]

    fig = px.line(
        filtered_df,
        x="Date",
        y="Sales",
        title="Pink Morsel Sales Over Time",
        labels={"Sales": "Sales ($)", "Date": "Date"},
    )
    fig.add_vline(
        x=pd.Timestamp("2021-01-15"),
        line_width=2,
        line_dash="dash",
        line_color="red",
    )
    return fig


if __name__ == "__main__":
    app.run(debug=True)

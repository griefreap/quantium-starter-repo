import pandas as pd
import dash
from dash import dcc, html, Input, Output
import plotly.express as px

# Load and prepare data
df = pd.read_csv("cleaned_sales.csv")
df["Date"] = pd.to_datetime(df["Date"])

# Initialize app
app = dash.Dash(__name__)
app.title = "Pink Morsel Sales Dashboard"

# Color palette
BACKGROUND_COLOR = "#f8f9fa"
CARD_COLOR = "#ffffff"
TEXT_COLOR = "#333333"
ACCENT_COLOR = "#e63946"

# Layout
app.layout = html.Div(
    style={"fontFamily": "Arial, sans-serif", "backgroundColor": BACKGROUND_COLOR, "padding": "20px"},
    children=[
        html.H1(
            "Soul Foods: Pink Morsel Sales Visualiser",
            style={"textAlign": "center", "color": TEXT_COLOR, "marginBottom": "20px"}
        ),

        # Radio button for region selection
        html.Div(
            style={"textAlign": "center", "marginBottom": "20px"},
            children=[
                html.Label("Select a Region:", style={"fontWeight": "bold", "color": TEXT_COLOR}),
                dcc.RadioItems(
                    id="region-selector",
                    options=[
                        {"label": "All", "value": "all"},
                        {"label": "North", "value": "north"},
                        {"label": "East", "value": "east"},
                        {"label": "South", "value": "south"},
                        {"label": "West", "value": "west"}
                    ],
                    value="all",
                    labelStyle={"display": "inline-block", "marginRight": "20px"}
                )
            ]
        ),

        # Chart container
        html.Div(
            style={
                "maxWidth": "1000px",
                "margin": "0 auto",
                "backgroundColor": CARD_COLOR,
                "padding": "20px",
                "borderRadius": "10px",
                "boxShadow": "0 4px 8px rgba(0,0,0,0.1)"
            },
            children=[
                dcc.Graph(id="sales-line-chart")
            ]
        )
    ]
)

# Callback to update chart based on region
@app.callback(
    Output("sales-line-chart", "figure"),
    Input("region-selector", "value")
)
def update_chart(selected_region):
    # Filter data
    if selected_region == "all":
        filtered_df = df
    else:
        filtered_df = df[df["Region"] == selected_region]

    # Aggregate by date
    sales_by_date = filtered_df.groupby("Date")["Sales"].sum().reset_index()

    # Create line chart
    fig = px.line(
        sales_by_date,
        x="Date",
        y="Sales",
        labels={"Date": "Date", "Sales": "Total Sales ($)"},
        title=f"Pink Morsel Sales Over Time ({selected_region.capitalize()})",
        template="plotly_white"
    )

    # Add vertical line for price increase
    fig.add_shape(
        type="line",
        x0="2021-01-15",
        y0=0,
        x1="2021-01-15",
        y1=sales_by_date["Sales"].max() if not sales_by_date.empty else 0,
        line=dict(color=ACCENT_COLOR, width=2, dash="dash")
    )

    fig.add_annotation(
        x="2021-01-15",
        y=sales_by_date["Sales"].max() if not sales_by_date.empty else 0,
        text="Price Increase",
        showarrow=True,
        arrowhead=2,
        ax=0,
        ay=-40
    )

    fig.update_layout(
        margin={"l": 40, "r": 40, "t": 80, "b": 40},
        title_font=dict(size=20, color=TEXT_COLOR),
        font=dict(color=TEXT_COLOR)
    )

    return fig


# Run app
if __name__ == "__main__":
    app.run(debug=True)

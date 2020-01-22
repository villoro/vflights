"""
    Dash app
"""

import dash
import plotly.express as px
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

from data_loader import DFG

df = DFG[(DFG["Origin"] == "BCN") & (DFG["Destination"] == "CAG")]
df = df.sort_values("Inserted", ascending=False).drop_duplicates(["Date"])


APP = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

APP.layout = html.Div(
    children=[
        dbc.NavbarSimple(brand="VFlights", brand_href="#", color="primary", dark=True),
        dcc.Graph(id="plot_prices", figure=px.bar(df, x="Date", y="Price")),
        dbc.Row(
            [
                dbc.Col(
                    dcc.Graph(
                        id="plot_evolution",
                        figure={
                            "data": [
                                {"x": [1, 2, 3], "y": [4, 1, 2], "type": "bar", "name": "SF"},
                                {"x": [1, 2, 3], "y": [2, 4, 5], "type": "bar", "name": "Montréal"},
                            ],
                            "layout": {"title": "Dash Data Visualization"},
                        },
                    )
                ),
                dbc.Col(),
            ]
        ),
    ]
)


if __name__ == "__main__":
    APP.run_server(debug=True)

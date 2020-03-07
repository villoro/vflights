"""
    Dash App layout
"""

import dash
import plotly.express as px
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

from data_loader import DFG

df = DFG[(DFG["Origin"] == "BCN") & (DFG["Destination"] == "CAG")]
df = df.sort_values("Inserted", ascending=False).drop_duplicates(["Date"])

airports = DFG["Origin"].unique()


def get_options(iterable):
    """
        Populates a dash dropdawn from an iterable
    """
    return [{"label": x, "value": x} for x in iterable]


def get_layout():
    """ Creates the dash layout """

    return html.Div(
        children=[
            dbc.NavbarSimple(
                [
                    dbc.Button("Filter", id="b_open"),
                    dbc.Modal(
                        [
                            dbc.ModalHeader("Filters"),
                            dbc.ModalBody(
                                [
                                    html.H4("Origin"),
                                    dcc.Dropdown(options=get_options(airports), value="CAG"),
                                    html.Br(),
                                    html.H4("Destination"),
                                    dcc.Dropdown(options=get_options(airports), value="BCN"),
                                ]
                            ),
                            dbc.ModalFooter(dbc.Button("Close", id="b_close", className="ml-auto")),
                        ],
                        id="modal",
                    ),
                ],
                brand="VFlights",
                brand_href="#",
                color="primary",
                dark=True,
            ),
            dcc.Graph(id="plot_prices", figure=px.bar(df, x="Date", y="Price")),
            dbc.Row(
                [
                    dbc.Col(
                        dcc.Graph(
                            id="plot_evolution",
                            figure={
                                "data": [
                                    {"x": [1, 2, 3], "y": [4, 1, 2], "type": "bar", "name": "SF"},
                                    {
                                        "x": [1, 2, 3],
                                        "y": [2, 4, 5],
                                        "type": "bar",
                                        "name": "Montréal",
                                    },
                                ],
                                "layout": {"title": "Dash Data Visualization"},
                            },
                        )
                    ),
                    dbc.Col(
                        dcc.Graph(
                            id="plot_temp",
                            figure={
                                "data": [
                                    {"x": [1, 2, 3], "y": [1, 1, 2], "name": "x"},
                                    {"x": [1, 2, 3], "y": [1, 2, 8], "name": "y"},
                                ],
                                "layout": {"title": "Dash Data Visualization"},
                            },
                        )
                    ),
                ]
            ),
        ]
    )

"""
    Dash App layout
"""

import dash
import plotly.express as px
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

from data_loader import get_airports


def get_options(iterable):
    """
        Populates a dash dropdawn from an iterable
    """
    return [{"label": x, "value": x} for x in iterable]


def get_filters():
    """ Filters in the model callable from the nav bar """

    airports = get_options(get_airports())

    # Use a dict with title and element
    filters = {
        "Origin": dcc.Dropdown(id="origin", options=airports, value="CAG"),
        "Destination": dcc.Dropdown(id="dest", options=airports, value="BCN"),
        "Direct flights": dcc.RadioItems(
            id="direct",
            options=[
                {"label": "Direct", "value": "1"},
                {"label": "All", "value": "0"},
                {"label": "No direct", "value": "-1"},
            ],
            value="1",
            inputStyle={"margin-left": "20px"},
        ),
        "Show flights from past": dcc.RadioItems(
            id="past",
            options=[{"label": "Yes", "value": "1"}, {"label": "No", "value": "0"}],
            value="0",
            inputStyle={"margin-left": "20px"},
        ),
        "Carriers": dcc.Dropdown(id="carriers", multi=True),
        "Max price": dcc.Input(
            id="max_price", placeholder="Enter max price...", type="number", min=0
        ),
    }

    # Concat all titles, elements and spacers
    modal_body = []
    for title, element in filters.items():
        modal_body += [html.H4(title), element, html.Br()]

    # Return the whole model info
    return [
        dbc.ModalHeader("Filters"),
        dbc.ModalBody(modal_body),
        dbc.ModalFooter(dbc.Button("Close", id="b_close", className="ml-auto")),
    ]


def get_layout():
    """ Creates the dash layout """

    return html.Div(
        children=[
            dbc.NavbarSimple(
                [dbc.Button("Filter", id="b_open"), dbc.Modal(get_filters(), id="modal")],
                brand="VFlights",
                brand_href="#",
                color="primary",
                dark=True,
            ),
            dcc.Graph(id="plot_prices"),
            dbc.Row([dbc.Col(dcc.Graph(id="plot_evolution")), dbc.Col(dcc.Graph(id="plot_temp"))]),
        ]
    )

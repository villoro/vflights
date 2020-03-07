"""
    Dash app
"""

import dash
import plotly.express as px
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State

import plots
from data_loader import get_carriers
from layout import get_layout, get_options

APP = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])


APP.layout = get_layout()


@APP.callback(
    Output("modal", "is_open"),
    [Input("b_open", "n_clicks"), Input("b_close", "n_clicks")],
    [State("modal", "is_open")],
)
def toggle_modal(n1, n2, is_open):
    """ Open / Close the modal """

    if n1 or n2:
        return not is_open
    return is_open


@APP.callback(
    Output("plot_prices", "figure"),
    [Input(x, "value") for x in ["origin", "dest", "direct", "past", "carriers", "max_price"]],
)
def plot_prices(origin, dest, direct, past, carriers, max_price):
    """ Update the prices plot """

    return plots.prices(origin, dest, direct, past, carriers, max_price)


@APP.callback(
    Output("plot_evolution", "figure"),
    [Input(x, "value") for x in ["origin", "dest", "direct"]] + [Input("plot_prices", "clickData")],
)
def plot_evolution(origin, dest, direct, click_data):
    """ Update the evolution plot """

    # Extract day from clicked point
    day = None if click_data is None else click_data["points"][0]["x"]

    return plots.evolution(origin, dest, direct, day)


@APP.callback(
    Output("carriers", "options"), [Input(x, "value") for x in ["origin", "dest", "direct", "past"]]
)
def update_carriers(origin, dest, direct, past):
    """ Update the carriers list """

    return get_options(get_carriers(origin, dest, direct, past))


if __name__ == "__main__":
    APP.run_server(debug=True)

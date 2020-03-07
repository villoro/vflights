"""
    Dash app
"""

import dash
import plotly.express as px
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State

import plots
from layout import get_layout


APP = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])


APP.layout = get_layout()


@APP.callback(
    Output("modal", "is_open"),
    [Input("b_open", "n_clicks"), Input("b_close", "n_clicks")],
    [State("modal", "is_open")],
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open


@APP.callback(
    Output("plot_prices", "figure"),
    [
        Input("origin", "value"),
        Input("dest", "value"),
        Input("direct", "value"),
        Input("carriers", "value"),
        Input("past", "value"),
    ],
)
def toggle_modal(origin, dest, direct, carriers, past):

    # Cast numbers
    direct = int(direct)
    past = bool(int(past))

    return plots.prices(origin, dest, direct, carriers, past)


if __name__ == "__main__":
    APP.run_server(debug=True)

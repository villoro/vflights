"""
    Plots
"""

import pandas as pd
from datetime import datetime
import plotly.express as px

from data_loader import fitler_df


def prices(origin, dest, direct, past, carriers=None, max_price=None):
    """ Plot prices """

    df = fitler_df(origin, dest, direct, past, carriers, max_price)

    df = df.sort_values("Quote_date", ascending=False).drop_duplicates(["Date"])

    fig = px.bar(df, x="Date", y="Price", color="Carrier")
    return fig.for_each_trace(lambda t: t.update(name=t.name.split("=")[1]))


def evolution(origin, dest, direct, day=datetime.now()):
    """ Plot evolution of a given day """

    df = fitler_df(origin, dest, direct, past=False)

    df = df[pd.to_datetime(df["Date"]) == pd.to_datetime(day)]

    df = df.sort_values("Quote_date", ascending=False).drop_duplicates(["Inserted"])

    fig = px.bar(
        df, x="Inserted", y="Price", color="Carrier", title=f"Price evolution for {day:%Y/%m%d}"
    )
    return fig.for_each_trace(lambda t: t.update(name=t.name.split("=")[1]))

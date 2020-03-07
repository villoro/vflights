"""
    Plots
"""

import pandas as pd
from datetime import datetime
import plotly.express as px

from data_loader import fitler_df


def prices(origin, dest, direct, past, carriers=None, max_price=None):
    """ Plot prices """

    # Filter dataframe
    df = fitler_df(origin, dest, direct, past, carriers, max_price)

    # Drop duplicates and plot
    df = df.sort_values("Quote_date", ascending=False).drop_duplicates(["Date"])
    fig = px.bar(
        df, x="Date", y="Price", color="Carrier", title=f"From {origin} to {dest} by flight date"
    )
    return fig.for_each_trace(lambda t: t.update(name=t.name.split("=")[1]))


def evolution(origin, dest, direct, day):
    """ Plot evolution of a given day """

    if day is None:
        day = datetime.now()

    day = pd.to_datetime(day)

    # Filter dataframe
    df = fitler_df(origin, dest, direct, past=False)
    df = df[pd.to_datetime(df["Date"]) == day]

    # Drop duplicates and plot
    df = df.sort_values("Quote_date", ascending=False).drop_duplicates(["Inserted"])

    kwa = {
        "x": "Inserted",
        "y": "Price",
        "color": "Carrier",
        "title": f"Price evolution for {day:%Y/%m/%d}",
    }

    # One carrier do a line, else a bar plot by carrier
    if len(df["Carrier"].unique()) == 1:
        # In order to have natural lines sort by x axis
        df = df.sort_values("Inserted", ascending=False)
        return px.line(df, **kwa)

    fig = px.bar(df, **kwa)
    return fig.for_each_trace(lambda t: t.update(name=t.name.split("=")[1]))

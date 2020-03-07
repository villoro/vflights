"""
    Plots
"""

import pandas as pd
from datetime import datetime
import plotly.express as px

from data_loader import DFG


def fitler_df(origin, dest, direct, past, carriers=None, max_price=None):
    """ Generic function to filter a dataframe """

    df = DFG[(DFG["Origin"] == origin) & (DFG["Destination"] == dest)].copy()

    if carriers is not None:
        df = df[df["Carrier"].isin(carriers)]

    if not past:
        df = df[pd.to_datetime(df["Date"]) > datetime.now()]

    # If positive asking for direct flights
    if direct > 0:
        df = df[df["Direct"]]

    # If negative asking for non direct flights
    if direct < 0:
        df = df[~df["Direct"]]

    if max_price is not None:
        df = df[df["Price"] < max_price]

    return df


def prices(origin, dest, direct, past, carriers=None, max_price=None):
    """ Plot prices """

    df = fitler_df(origin, dest, direct, past, carriers, max_price)

    df = df.sort_values("Inserted", ascending=False).drop_duplicates(["Date"])

    return px.bar(df, x="Date", y="Price", color="Carrier")

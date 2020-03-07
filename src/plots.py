"""
    Plots
"""

import pandas as pd
from datetime import datetime
import plotly.express as px

from data_loader import DFG


def prices(origin, dest, direct, carriers, past):

    df = DFG[
        (DFG["Origin"] == origin)
        & (DFG["Destination"] == dest)
        & (DFG["Direct"] == direct)
        & (DFG["Carrier"].isin(carriers))
    ].copy()

    print(past)

    if not past:
        print("Filtering")
        df = df[pd.to_datetime(df["Date"]) > datetime.now()]

    # If positive asking for direct flights
    if direct > 0:
        df = df[df["Direct"]]

    # If negative asking for non direct flights
    if direct < 0:
        df = df[~df["Direct"]]

    df = df.sort_values("Inserted", ascending=False).drop_duplicates(["Date"])

    return px.bar(df, x="Date", y="Price")

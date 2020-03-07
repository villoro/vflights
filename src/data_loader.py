"""
    Utilities for input/output operations.
    It is important to have DFS as global variable in this class to take advantatges of singeltons

    Info: https://python-3-patterns-idioms-test.readthedocs.io/en/latest/Singleton.html

    All pages can import this file and retrive data by:

        > from data_loader import DFS
        > df_xx = DFS[xx] # xx is the name of the dataframe
"""

import io
from datetime import datetime

import dropbox
import pandas as pd
import oyaml as yaml

import constants as c
import utilities as u


DBX = dropbox.Dropbox(u.get_secret(c.VAR_DROPBOX_TOKEN))

DFG = None


def sync():
    """
        Read an excel from dropbox as a pandas dataframe
    """

    global DFG

    _, res = DBX.files_download(c.FILE_FLIGHTS)
    DFG = pd.read_excel(io.BytesIO(res.content))


# Do one sync when it is imported!
sync()


def fitler_df(origin, dest, direct, past, carriers=None, max_price=None):
    """ Generic function to filter a dataframe """

    df = DFG[(DFG["Origin"] == origin) & (DFG["Destination"] == dest)].copy()

    if carriers is not None:
        df = df[df["Carrier"].isin(carriers)]

    if not bool(int(past)):
        df = df[pd.to_datetime(df["Date"]) > datetime.now()]

    # If positive asking for direct flights
    if int(direct) > 0:
        df = df[df["Direct"]]

    # If negative asking for non direct flights
    if int(direct) < 0:
        df = df[~df["Direct"]]

    if max_price is not None:
        df = df[df["Price"] < max_price]

    return df


def get_carriers(origin, dest, direct, past):
    """ Get list of possible carriers """

    df = fitler_df(origin, dest, direct, past)
    return df["Carrier"].unique().tolist()


def get_airports():
    """ Get list of possible airports """

    return DFG["Origin"].unique().tolist()

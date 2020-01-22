"""
    Utilities for input/output operations.
    It is important to have DFS as global variable in this class to take advantatges of singeltons

    Info: https://python-3-patterns-idioms-test.readthedocs.io/en/latest/Singleton.html

    All pages can import this file and retrive data by:

        > from data_loader import DFS
        > df_xx = DFS[xx] # xx is the name of the dataframe
"""

import io

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

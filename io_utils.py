import pandas as pd
from time import strftime

def dumps_like_a_truck(dataframe, filename=None, append=False):
    """Saves collected dataframe to a serialized pickle format"""

    if filename is None:
        filename = "./data/" + strftime("%m_%d_%y.%H.%M.%S") + ".pkl"

    dataframe.to_pickle(filename, append=append)


def pick_it_up(filename):
    """Loads a saved pickle file
    By default it creates a new dataframe named after the file"""

    return pd.read_pickle(filename)

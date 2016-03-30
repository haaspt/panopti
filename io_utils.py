import pandas as pd
from time import strftime

def dumps_like_a_truck(dataframe, filename=None, append=False):
    """Saves collected dataframe to a serialized format
    Currently this uses the pandas experimental msgpack binary format
    
    This may be edited in the future if it proves problematic"""
    
    if filename is None:
        filename = "./data/" + strftime("%m_%d_%y.%H.%M.%S") + ".msg"

    dataframe.to_msgpack(filename, append=append)


def pick_it_up(filename):
    """Loads a saved msgpack
    By default it creates a new dataframe named after the file"""

    return pd.read_msgpack(filename)

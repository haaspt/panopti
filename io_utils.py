import re
import pandas as pd
from time import strftime

def dumps_like_a_truck(dataframe, filename=None):
    """Saves collected dataframe to a serialized format
    Currently this uses the pandas experimental msgpack binary format
    
    This may be edited in the future if it proves problematic"""

    filename = strftime("%m_%d_%y.%H.%M.%S") + ".msg"
    
    dataframe.to_msgpack(filename)


def pick_it_up(filename):
    """Loads a saved msgpack
    By default it creates a new dataframe named after the file"""

    return pd.read_msgpack(filename)

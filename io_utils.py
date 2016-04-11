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


def load_log(filename="./log/log_file.pkl"):

    try:
        log_file = pd.read_pickle(filename)
    except:
        print("No log file found. Creating new log file...")
        log_file = pd.DataFrame()

    return log_file


def save_log(log_dataframe, filename="./log/log_file.pkl")

    log_dataframe.to_pickle(filename)
    print("Log file saved to disk!")

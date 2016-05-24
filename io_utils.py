#!/usr/local/bin/env python
import pandas as pd
from time import strftime

def dumps_like_a_truck(dataframe, filename=None):
    """Saves collected dataframe to a serialized pickle format"""

    if filename is None:
        filename = "/home/pi/Developer/panopti/data/" + strftime("%m_%d_%y.%H.%M.%S") + ".pkl"

    dataframe.to_pickle(filename)


def pick_it_up(filename):
    """Loads a saved pickle file
    By default it creates a new dataframe named after the file"""

    return pd.read_pickle(filename)


def load_log(filename="/home/pi/Developer/panopti/log/user_log.pkl"):

    try:
        log_file = pd.read_pickle(filename)
    except:
        print("No log file found. Creating new log file...")
        log_file = pd.DataFrame(colums=['object_type','post_id','post_timestamp','user_name'])

    return log_file


def save_log(log_dataframe, filename="/home/pi/Developer/panopti/log/user_log.pkl"):

    log_dataframe.to_pickle(filename)
#    print("Log file saved to disk!")

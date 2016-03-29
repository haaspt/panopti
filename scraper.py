import praw
import json
import pandas as pd
import numpy as np
from config import GlobalConfig
from __future__ import print_function, division

def reddit_init():
    reddit = praw.Reddit(user_agent = GlobalConfig.user_agent)
    reddit.config.store_json_result = True

def get_feed():
    top_hub_submissions = reddit.get_submissions(GlobalConfig.network_hub).get_top(limit = 1000)
    return top_hub_submissions

def iterator(submission_generator_object):
    for post in submission_generator_object:
        # Do something

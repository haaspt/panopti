from __future__ import print_function, division
import praw
import pandas as pd
from config import Config

option = Config()

def reddit_init():
    reddit = praw.Reddit(user_agent = option.user_agent)
    reddit.config.store_json_result = True

def get_feed():
    top_hub_submissions = reddit.get_submissions(option.network_hub).get_top(limit = 1000)
    return top_hub_submissions

"""
def iterator(submission_generator_object):
    for post in submission_generator_object:
        # Do something
"""

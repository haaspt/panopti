import io_utils
import scraper
from __future__ import print_function, division
import praw
import pandas as pd
from config import GlobalConfig

options = GlobalConfig()
reddit = praw.Reddit(user_agent = options.user_agent)

new_posts = reddit.get_subreddit(options.network_hub).get_new(limit=1000)

def get_new_authors(post_list, author_list=None):
    """Basic syntax to gather a list of post and comment authors
    gathered from new posts on the target subreddit

    To Do:
    - More structured data processing
    - Display counter
    - Maybe flatten the comment tree?
    """

    if not author_list:
        author_list = []

    for post in post_list:
        author_list.append(post.author)
        for comment in post.comment:
            author_list.append(comment.author)

    return author_list

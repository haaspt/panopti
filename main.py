from __future__ import print_function, division
import io_utils
import scraper
import praw
import pandas as pd
from config import GlobalConfig

options = GlobalConfig()
reddit = praw.Reddit(user_agent = options.user_agent)

new_posts = reddit.get_subreddit(options.network_hub).get_new(limit=10)

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

    counter = 0

    for post in post_list:
        author_list.append(post.author)
        counter += 1
        print("Authors added: %d" % counter, end="\r")
        for comment in post.comments:
            author_list.append(comment.author)
            counter += 1
            print("Authors added: %d" % counter, end="\r")

    return author_list

def get_user_comments(username):
    # I'm fairly positive this doesn't actually work
    user_comments = user.get_submitted(limit=10)

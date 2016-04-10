from __future__ import print_function, division
import io_utils
import scraper
import praw
import pandas as pd
from config import Config

options = Config()
reddit = praw.Reddit(user_agent = options.user_agent)

new_posts = reddit.get_subreddit(options.network_hub).get_new(limit=options.post_limit)

def get_new_authors(post_generator, author_list=None):
    """Basic syntax to gather a list of post and comment authors
    gathered from new posts on the target subreddit

    To Do:
    - More structured data processing
    - Maybe flatten the comment tree?
    """

    if not author_list:
        author_list = []

    for post in post_generator:
        author_list.append(post.author.name)
        for comment in post.comments:
            author_list.append(comment.author.name)

    author_df = pd.DataFrame({'user_name': author_list, 'highest_post_id': ""})
    author_df = author_df.drop_duplicates('user_name')
    print('%d new authors found!' % (len(author_df.user_name)))
    return author_df

def get_user_comments(username):
    # I'm fairly positive this doesn't actually work
    user_comments = user.get_submitted(limit=10)

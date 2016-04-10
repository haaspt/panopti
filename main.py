from __future__ import print_function, division
import time
import io_utils
import scraper
import praw
import pandas as pd
from config import Config

options = Config()
reddit = praw.Reddit(user_agent = options.user_agent)

new_posts = reddit.get_subreddit(options.network_hub).get_new(limit=options.post_limit)

def get_new_authors(reddit_post_generator, author_list=None):
    """Basic syntax to gather a list of post and comment authors
    gathered from new posts on the target subreddit

    To Do:
    - More structured data processing
    - Maybe flatten the comment tree?
    """

    if not author_list:
        author_list = []

    for post in reddit_post_generator:
        author_list.append(post.author.name)
        for comment in post.comments:
            author_list.append(comment.author.name)

    author_df = pd.DataFrame({'user_name': author_list, 'highest_post_id': ""})
    author_df = author_df.drop_duplicates('user_name')
    print('%d new authors found!' % (len(author_df.user_name)))
    return author_df

def comment_parser(reddit_comment_object):

    post_timestamp = reddit_comment_object.created_utc
    post_id = reddit_comment_object.id
    score = reddit_comment_object.score
    ups = reddit_comment_object.ups
    downs = reddit_comment_object.downs
    post_body = reddit_comment_object.body
    link_title = reddit_comment_object.link_title
    link_id = reddit_comment_object.link_id
    link_author = reddit_comment_object.link_author
    subreddit = reddit_comment_object.subreddit.display_name

    return post_timestamp, post_id, score, ups, downs, post_body, link_title, link_id, link_author, subreddit


def get_user_comments(reddit_user_object, comment_dataframe=None):

    user_name = reddit_user_object.name
    user_comments = reddit_user_object.get_comments(limit=1000) # Due to reddit's caching, 1000 is the absolute max

    if not comment_dataframe:
        comment_dataframe = pd.DataFrame(columns=[
        'user_name',
        'post_timestamp',
        'post_id',
        'score',
        'ups',
        'downs',
        'post_body',
        'link_title',
        'link_id',
        'link_author',
        'subreddit',
        'timestamp'
        ])

    for comment in user_comments:
        post_timestamp, post_id, score, ups, downs, post_body, link_title, link_id, link_author, subreddit = comment_parser(comment)
        comment_dataframe = comment_dataframe.append({
        'user_name': user_name,
        'post_timestamp': post_timestamp,
        'post_id': post_id,
        'score': score,
        'ups': ups,
        'downs': downs,
        'post_body': post_body,
        'link_title': link_title,
        'link_id': link_id,
        'link_author': link_author,
        'subreddit': subreddit,
        'timestamp': time.time()}, ignore_index=True)

    return comment_dataframe

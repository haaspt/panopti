from __future__ import print_function, division
import time
import io_utils
import scraper
import praw
import pandas as pd
import numpy as np
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
    thread_title = reddit_comment_object.link_title
    thread_url = reddit_comment_object.link_url
    subreddit = reddit_comment_object.subreddit.display_name

    return post_timestamp, post_id, score, ups, downs, post_body, thread_title, thread_url, subreddit


def submission_parser(reddit_submission_object):

    post_timestamp = reddit_submission_object.created_utc
    post_id = reddit_submission_object.id
    score = reddit_submission_object.score
    ups = reddit_submission_object.ups
    downs = reddit_submission_object.downs
    # post_body = np.nan
    thread_title = reddit_submission_object.title
    thread_url = reddit_submission_object.url
    subreddit = reddit_submission_object.subreddit.display_name

    return post_timestamp, post_id, score, ups, downs, thread_title, thread_url, subreddit


def get_user_comments(reddit_user_object, content_dataframe=None):

    user_name = reddit_user_object.name
    user_comments = reddit_user_object.get_comments(limit=1000) # Due to reddit's caching, 1000 is the absolute max

    if content_dataframe is None:
        content_dataframe = pd.DataFrame(columns=[
        'object_type',
        'user_name',
        'post_timestamp',
        'post_id',
        'score',
        'ups',
        'downs',
        'post_body',
        'thread_title',
        'thread_url',
        'subreddit',
        'timestamp'
        ])

    for comment in user_comments:
        post_timestamp, post_id, score, ups, downs, post_body, thread_title, thread_url, subreddit = comment_parser(comment)
        content_dataframe = content_dataframe.append({
        'object_type': 'comment',
        'user_name': user_name,
        'post_timestamp': post_timestamp,
        'post_id': post_id,
        'score': score,
        'ups': ups,
        'downs': downs,
        'post_body': post_body,
        'thread_title': thread_title,
        'thread_url': thread_url,
        'subreddit': subreddit,
        'timestamp': time.time()}, ignore_index=True)

    return content_dataframe


def get_user_submissions(reddit_user_object, content_dataframe=None):

    user_name = reddit_user_object.name
    user_submissions = reddit_user_object.get_submitted(limit=1000) # Due to reddit's caching, 1000 is the absolute max

    if content_dataframe is None:
        content_dataframe = pd.DataFrame(columns=[
        'object_type',
        'user_name',
        'post_timestamp',
        'post_id',
        'score',
        'ups',
        'downs',
        'post_body',
        'thread_title',
        'thread_url',
        'subreddit',
        'timestamp'
        ])

    for submission in user_submissions:
        post_timestamp, post_id, score, ups, downs, thread_title, thread_url, subreddit = submission_parser(submission)
        content_dataframe = content_dataframe.append({
        'object_type': 'submission',
        'user_name': user_name,
        'post_timestamp': post_timestamp,
        'post_id': post_id,
        'score': score,
        'ups': ups,
        'downs': downs,
        'post_body': np.nan,
        'thread_title': thread_title,
        'thread_url': thread_url,
        'subreddit': subreddit,
        'timestamp': time.time()}, ignore_index=True)

    return content_dataframe

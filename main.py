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

def get_new_authors(reddit_post_generator, author_series=None):
    """Takes a reddit post generator object and an optional pandas series.
    Iterates through the generator and adds praw user objects to the series
    if the author has not already been added.

    Returns: pd.series
    """

    if author_series is None:
        author_series = pd.Series()

    for post in reddit_post_generator:
        if post.author not in author_series.values:
            author_series = author_series.append(pd.Series(post.author))
        for comment in post.comments:
            if comment.author not in author_series.values:
                author_series = author_series.append(pd.Series(comment.author))

    return author_series

def log_author(reddit_user_object):
    """Takes a praw user object and fetches their highest comment and submission
    which can then be appended to the user log for caching purposes.

    Returns: dict
    """

    user_name = reddit_user_object.name

    newest_submission = reddit_user_object.get_submitted().next()
    newest_submission_id = newest_submission.id
    newest_submission_timestamp = newest_submission.created

    newest_comment = reddit_user_object.get_comments().next()
    newest_comment_id = newest_comment.id
    newest_comment_timestamp = newest_comment.created

    user_log_entry = {
    'user_name': user_name,
    'newest_submission_id': newest_comment_id,
    'newest_submission_timestamp': newest_submission_timestamp,
    'newest_comment_id': newest_comment_id,
    'newest_comment_timestamp': newest_comment_timestamp,
    'last_searched': time.time()
    }

    return user_log_entry


def comment_parser(reddit_comment_object):
    """Parses a comment and returns selected parameters"""

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
    """Parses a submission and returns selected parameters"""

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
    """Takes a praw user object and iterates through his/her comment history.
    Certain comment parameters are parsed are appended to a pandas dataframe.

    Takes and optional content_dataframe

    Returns content_dataframe
    """

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
    """Takes a praw user object and iterates through his/her submission history.
    Certain comment parameters are parsed are appended to a pandas dataframe.

    Takes and optional content_dataframe

    Returns content_dataframe
    """

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

#!/usr/local/bin/env python
from __future__ import print_function
import io_utils
import scraper
import praw
import pandas as pd
from config import Config


def main():

    options = Config()
    reddit = praw.Reddit(user_agent = options.user_agent)
    reddit.login('MrPrimeMover', '7654957', disable_warning=True)
    
    post_generator = reddit.get_subreddit(options.network_hub).get_new(limit=options.post_limit)
    user_series = scraper.get_new_authors(post_generator)
    content_df = pd.DataFrame(columns=['downs', 'object_type', 'post_body',
    'post_id', 'post_timestamp', 'score', 'subreddit', 'thread_title',
    'thread_url', 'timestamp', 'ups', 'user_name'])
    log_df = io_utils.load_log()
    for user in user_series:
        if not (log_df.user_name.ix[log_df.object_type == 'comment'] == user.name).any():
            #Check if user already has a comment logged in the log dataframe
            content_df = scraper.get_user_comments(user, content_dataframe=content_df)

        if not (log_df.user_name.ix[log_df.object_type == 'submission'] == user.name).any():
            # Check if user already has a submission logged in the log dataframe
            content_df = scraper.get_user_submissions(user, content_dataframe=content_df)

    # Logging syntax needs to be steamlined...
    new_users_to_log = content_df[['user_name', 'object_type', 'post_id', 'post_timestamp']].ix[content_df.groupby(['user_name', 'object_type']).post_timestamp.idxmax()]
    log_df = log_df.append(new_users_to_log)
    log_df = log_df.reset_index(drop=True)
    io_utils.save_log(log_df)

    io_utils.dumps_like_a_truck(content_df)

#    print("Logged %d new users!" % len(new_users_to_log.user_name.unique()))
#    print("Logged %d new posts!" % len(content_df))

if __name__ == "__main__":
    main()

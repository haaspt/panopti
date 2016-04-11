from __future__ import print_function
import time
import io_utils
import scraper
import praw
import pandas as pd
from config import Config


def main():

    options = Config()
    reddit = praw.Reddit(user_agent = options.user_agent)

    post_generator = reddit.get_subreddit(options.network_hub).get_top(limit=options.post_limit)

    user_series = scraper.get_new_authors(post_generator)
    content_df = pd.DataFrame()
    log_df = io_utils.load_log()

    for user in user_series: #Look up proper pd.series iteration syntax
        content_df = scraper.get_user_comments(user, content_dataframe=content_df)
        content_df = scraper.get_user_submissions(user, content_dataframe=content_df)

        log_df = scraper.log_user(user, log_dataframe=log_df)

    io_utils.dumps_like_a_truck(content_df)
    io_utils.save_log(log_df)


if __name__ == "main":
    main()

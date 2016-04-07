#===========================
# General Configuration
#===========================

class Config(object):
    """Basic configuration"""

    def reddit_config(self):
        self.network_hub =  "all" # Replace with subreddit name (the part after /r/)
        self.user_agent = "Social network mapper, monitored by /u/YourUserName"

    def scraper_config(self):
        self.post_limit = 100 # Max number of new posts to search for

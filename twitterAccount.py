#twitter.py
import os
import twitter
from dotenv import load_dotenv

# Authenticate Twitter API
load_dotenv()
CONSUMER_KEY = os.getenv('TWITTER_API_KEY')
CONSUMER_SECRET = os.getenv('TWITTER_API_SECRET_KEY')
OAUTH_TOKEN = os.getenv('TWITTER_ACCESS_TOKEN')
OAUTH_TOKEN_SECRET = os.getenv('TWITTER_ACCESS_TOKEN_SECRET')

auth = twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET,
                        CONSUMER_KEY, CONSUMER_SECRET)

twitter_api = twitter.Twitter(auth=auth)

# A class describing Twitter accounts
class TwitterAccount():

    # initializes Twitter account objects
    def __init__(self, name, frequency):
        self.username = name
        self.freq = frequency
        self.since = None

    # Get List of tweets since lastID for a specified TwitterAccount
    def getTweets(self) -> list:

        # Get user_timeline
        # https://developer.twitter.com/en/docs/tweets/timelines/api-reference/get-statuses-user_timeline
        # optionally can add parameter 'exclude_replies=True' to get rid of self-replies
        if self.since:
            tweets_data = twitter_api.statuses.user_timeline(count=self.freq,
                                                        screen_name=self.username, include_rts=False, since_id=self.since)
        else:
                        tweets_data = twitter_api.statuses.user_timeline(count=self.freq,
                                                        screen_name=self.username, include_rts=False)
        tweets_list = []
        for tweet in tweets_data:
            tweets_list.insert(0, 'https://twitter.com/twitter/statuses/' + str(tweet['id']))
            # To display text, created at time, and tweet id, uncomment the following line and comment the one above
            # tweets_list.append(tweet['text'] + '\n' + tweet['created_at'] + '\n' + 'https://twitter.com/twitter/statuses/' + str(tweet['id']))

        # update sinceID if new tweets have been retrieved
        if tweets_data:
            self.since = tweets_data[0]['id']

        # For debugging purposes, below line prints current account's tweets list
        # print(tweets_list)
        return tweets_list

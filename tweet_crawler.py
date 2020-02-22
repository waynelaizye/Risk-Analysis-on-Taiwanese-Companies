import os
import tweepy as tw
import pandas as pd

ACCESS_TOKEN = '1288560438-SHG2abKSS9EFU3U6Uz2SdIDNaJcECoJhbUlfDgT'     # your access token
ACCESS_TOKEN_SECRET = 'Ol3RvqVkNk5qA1hNftpZ7WuMMnaEyhVjxWVkfXOskKegi'    # your access token secret
CONSUMER_KEY = 'KIPwjwW1UeY6TRHQ4a85yHL18'     # your API key
CONSUMER_SECRET = 'YUZFZhOwqp30XQ2MVzuQoZmvw50HK90IlRuEMaP0saxNGZDmfZ'  # your API secret key

def init():
    auth = tw.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    api = tw.API(auth, wait_on_rate_limit=True)

    return api

def post(api=None):
    api.update_status("Look, I'm tweeting from #Python in my #earthanalytics class! @EarthLabCU")


def search():
    # Define the search term and the date_since date as variables
    search_words = "#disk"
    date_since = "2019-11-16"


    # Collect tweets
    tweets = tw.Cursor(api.search,
              q=search_words,
              lang="en",
              since=date_since).items(100)
    
    for tweet in tweets:
        print(tweet.text)



if __name__== "__main__":
    api = init()
    #post(api)
    search()



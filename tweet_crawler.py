# This file is used to retrieve posts from twitter.
#
# Usage: 
# python tweet_crawler.py computer_peripherals.csv ./global_industry/
#
#


import os
import csv
import sys
import tweepy as tw
import pandas as pd
import pickle

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


def search(search_words="null", chosen_lang="en"):
    # Define the search term and the date_since date as variables
    date_since = "2019-03-03"
    
    print('search word: {0}'.format(search_words))
    message = []
    if search_words == "null" or search_words == "":
        return None 

    # Collect tweets
    tweets = tw.Cursor(api.search,
              q=search_words,
              lang=chosen_lang,
              since=date_since).items(50)
    
    for tweet in tweets:
        #print(tweet.text)
        message.append(tweet.text)
    #print(message)

    return message


def parse_csv(file_name = "None", dest_path = "./"):
    with open(file_name) as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        for row in readCSV:
            print(row)
            if len(row) == 0:
                break
            if len(row) > 1:
                data = {}
                msg0 = search(row[0], "zh-tw")
                if msg0 != None:
                    data[row[0]] = msg0
                    save_data(data, row[0], dest_path, "zh-tw")
                
                data = {}
                msg1 = search(row[1], "en")
                if msg1 != None:
                    data[row[1]] = msg1
                    save_data(data, row[1], dest_path, "en")
       
                data = {}
                msg2 = search(row[2], "en")
                if msg2 != None:
                    data[row[2]] = msg2
                    save_data(data, row[1], dest_path, "en")

    return True


def save_data(data, file_name, path, lang="eng"):
    file_name = file_name.replace(" ", "_")
    file_name = file_name.replace("/", "")
    print('file name = {0}'.format(file_name))
    dataset = path + "train_" + file_name + lang + ".data"

    with open(dataset, 'wb') as filehandle:
        pickle.dump(data, filehandle)


if __name__== "__main__":
    api = init()
    #post(api)
    #search()

    data = parse_csv(sys.argv[1], sys.argv[2])




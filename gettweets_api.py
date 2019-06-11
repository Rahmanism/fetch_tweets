# Gets some tweets with the given hashtag

# 1. We are going to collect tweets with special hashtags for building
#    a good enough data set for a linguistics project.
# 2. We use the data set for machine learning mechanism,
#    both with supervised and unsupervised methods.
# 3. Conceptual metaphor analyses may use the results of our project
#    to come up with how people understand and talk about different things.
# 4. App use description: We will search tweets with special hashtags
#    to create data sets that will be used for machine learning
#    in the field of cognitive linguistics.

# put twitter consumer secret keys here...

# App use description: Your Use Description!!
# api_key: 'yourapikeyoi34u759847tkdfjhgeiroytu'
# api_secret_key: 'yourapisecretkey2398457dhfj384957uoerhhg'
# access_token: 'anaccesstokenfullofj2347adoi23uy489dkfjgh38945y'
# access_token_secret: 'asecretaccesstokenfullof23894789andksdjfghaqleu'
# dev_environment_label: 'somecodefordevenvironmentlabel'

# my secrets are in the following file :)
from gettweets_secret_keys import *

import sys
import tweepy
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import gettweets_help
from db import DB

if '-h' in sys.argv or '--help' in sys.argv:
    gettweets_help.show_help()
    sys.exit(0)

try:
    tdb = DB()
except Exception as err:
    print(err)
    sys.exit(1)

tdb.check_create_db()

if len(sys.argv) > 1:
    hashtag = sys.argv[1]
else:
    hashtag = input('What\'s the hashtag you looking for? ')

# if '-top' in sys.argv:
#     url = 'https://twitter.com/hashtag/%s?lang=fa' % hashtag
# else:
#     url = 'https://twitter.com/hashtag/%s?f=tweets&lang=fa' % hashtag

auth = tweepy.OAuthHandler(api_key, api_secret_key)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)
 
inserted_tweets_count = 0
for tweet in tweepy.Cursor(api.search, q=f"#{hashtag}", lang="fa").items(10):
    print(tweet)
sys.exit()

def t():
    tweet_timestamp_tag = tweet.find('a', {'class': 'tweet-timestamp'})
    tweet_id = tweet_timestamp_tag.get('data-conversation-id')
    if tdb.check_if_exists(tweet_id):
        pass #continue
    tweet_timestamp = int(tweet_timestamp_tag.find(
        'span', {'class': '_timestamp'}).get('data-time'))
    tweet_time = datetime.fromtimestamp(tweet_timestamp)
    user = tweet.find('span', {'class': 'username'}).find('b').text
    tweet_content = tweet.find(
        'div', {'class': 'js-tweet-text-container'}).text
    reply = tweet.find('div', {'class': 'ReplyingToContextBelowAuthor'})
    tweet_type = 0 if reply == None else 1
    tweet_profile = tweet.find(
        'div', {'class': 'ProfileTweet-actionCountList'})
    replys = (tweet_profile.find(
        'span', {'class': 'ProfileTweet-action--reply'})
        .find('span', {'class': 'ProfileTweet-actionCount'})
        .get("data-tweet-stat-count"))
    retweets = (tweet_profile.find(
        'span', {'class': 'ProfileTweet-action--retweet'})
        .find('span', {'class': 'ProfileTweet-actionCount'})
        .get("data-tweet-stat-count"))
    likes = (tweet_profile.find(
        'span', {'class': 'ProfileTweet-action--favorite'})
        .find('span', {'class': 'ProfileTweet-actionCount'})
        .get("data-tweet-stat-count"))

    tweet_data = {
        'tweet_id': tweet_id,
        'user': user,
        'tweet': tweet_content,
        'tweet_type': tweet_type,
        'hashtag': hashtag,
        'timestamp_seconds': tweet_timestamp,
        'tweet_time': tweet_time,
        'likes': likes,
        'retweets': retweets,
        'replys': replys
    }
    tdb.insert_tweet(tweet_data)
    inserted_tweets_count += 1

del tdb
print(f"Number of tweets inserted in DB: {inserted_tweets_count}.")

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
from gettweets_api_help import *
from db_api import DB
from csv_api import CSV

if '-h' in sys.argv or '--help' in sys.argv:
    show_help()
    sys.exit(0)

if '-x' in sys.argv:
    try:
        csv_filename = sys.argv[sys.argv.index('-x') + 1]
    except:
        csv_filename = None
    csv = CSV(csv_filename)
    csv.export()
    sys.exit(0)

try:
    tdb = DB()
except Exception as err:
    print(err)
    sys.exit(1)

tdb.check_create_db()

# if '-top' in sys.argv:
#     url = 'https://twitter.com/hashtag/%s?lang=fa' % hashtag
# else:
#     url = 'https://twitter.com/hashtag/%s?f=tweets&lang=fa' % hashtag

auth = tweepy.OAuthHandler(api_key, api_secret_key)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

if '-hg' in sys.argv:
    hashtag = sys.argv[sys.argv.index('-hg') + 1]
else:
    hashtag = input('What\'s the hashtag you looking for? ')
print(f"#{hashtag} will be searched.")

number_of_tweets = 10
if '-c' in sys.argv:
    try:
        number_of_tweets = int(sys.argv[sys.argv.index('-c') + 1])
    except:
        print("Number of tweets isn't acceptable. The default (10) will be used.")

search_language = None
if '-l' in sys.argv:
    try:
        search_language = sys.argv[sys.argv.index('-l') + 1]
    except:
        print("No suitable language is selected!")

print("Gettings tweets...\n")
if search_language is None:
    tweets = tweepy.Cursor(api.search, q=f"#{hashtag}").items(number_of_tweets)
else:
    tweets = tweepy.Cursor(api.search, q=f"#{hashtag}",
                  lang=search_language).items(number_of_tweets)

inserted_tweets_count = 0
for tweet in tweets:
    print("Checking a tweet...")
    # print("\n==================================\n")
    # print(json.dumps(tweet._json))
    if tdb.check_if_exists(tweet._json['id_str']):
        print("It was duplicate.")
        continue
    tweet_data = {
        'tweet_id': tweet._json['id_str'],
        'username': tweet._json['user']['name'],
        'user_screen_name': tweet._json['user']['screen_name'],
        'user_id': tweet._json['user']['id_str'],
        'tweet': tweet._json['text'],
        'location': tweet._json['user']['location'],
        'searched_hashtag': hashtag,
        'created_at': tweet._json['created_at'],
        'favorite_count': tweet._json['favorite_count'],
        'retweet_count': tweet._json['retweet_count'],
    }
    print(f"Tweet No. {inserted_tweets_count} is being saved...")
    tdb.insert_tweet(tweet_data)
    inserted_tweets_count += 1

del tdb
print(f"\nNumber of tweets inserted in DB: {inserted_tweets_count}.\n")

# -*- coding: utf-8 -*-

# Export data to csv file.
import csv
import os
from db_api import DB
import sys


class CSV:
    def __init__(self, filename):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        defult_filename = f"{dir_path}/tweets.csv"
        self.last_tweet_id_filename = f"{dir_path}/last_tweet_id"
        if filename is None:
            self.csv_filename = defult_filename
        else:
            self.csv_filename = filename.strip()
        print(self.csv_filename)

    def export(self, filename=None, limit=None, full=False, hashtag=None):
        if filename is not None:
            self.csv_filename = filename.strip()

        try:
            tdb = DB()
        except Exception as err:
            print(err)
            sys.exit(1)

        # Open/Create a file to append data
        csv_file = open(self.csv_filename, 'w', encoding='utf-8', newline='')
        # Use csv Writer
        csv_writer = csv.writer(csv_file)

        if hashtag is not None:
            self.last_tweet_id_filename = f"{self.last_tweet_id_filename}_{hashtag}"
            
        last_tweet_id = 0
        if limit == 0:
            try:
                last_tweet_id_file = open(self.last_tweet_id_filename,
                                        'r', encoding='utf-8')
                last_tweet_id = int(last_tweet_id_file.read().strip())
                last_tweet_id_file.close()
            except:
                last_tweet_id = 0
        
        tweets = tdb.get_all_tweets(limit, last_tweet_id, hashtag)
        
        if full:
            csv_writer.writerow(['id', 'tweet_id', 'username', 'user_screen_name',
                                 'user_id', 'tweet', 'location', 'searched_hashtag',
                                 'created_at', 'retweet_count', 'favorite_count'])
            for tweet in tweets:
                print(tweet)
                print("------------------------------------")
                csv_writer.writerow(tweet)
        else:
            csv_writer.writerow(['tweet'])
            for tweet in tweets:
                print(tweet)
                print("------------------------------------")
                csv_writer.writerow(tweet[5])
        csv_file.close()
        
        last_tweet_id_file = open(self.last_tweet_id_filename, 'w', encoding='utf-8', newline='')
        if len(tweets) > 0:
            last_tweet_id_file.write(str(tweets[0][0]))
        last_tweet_id_file.close()

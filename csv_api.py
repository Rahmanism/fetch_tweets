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
        if filename is None:
            self.csv_filename = defult_filename
        else:
            self.csv_filename = filename.strip()
        print(self.csv_filename)

    def export(self, filename=None):
        if filename is not None:
            self.csv_filename = filename.strip()

        try:
            tdb = DB()
        except Exception as err:
            print(err)
            sys.exit(1)

        # Open/Create a file to append data
        csv_file = open(self.csv_filename, 'w')
        # Use csv Writer
        csv_writer = csv.writer(csv_file)

        tweets = tdb.get_all_tweets()
        csv_writer.writerow(['id', 'tweet_id', 'username', 'user_screen_name',
                            'user_id', 'tweet', 'location', 'searched_hashtag',
                            'created_at', 'retweet_count', 'favorite_count'])
        for tweet in tweets:
            print(tweet)
            print("------------------------------------")
            csv_writer.writerow((t.encode('utf-8') if type(t) is str else t for t in tweet))
        csv_file.close()

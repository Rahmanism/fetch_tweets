# -*- coding: utf-8 -*-

import mysql.connector
from mysql.connector import errorcode


class DB:
    def __init__(self):
        self.cnx = self.db_connect()
        self.cur = self.cnx.cursor()

    def __del__(self):
        try:
            self.cur.close()
            self.cnx.close()
        except:
            pass

    def db_connect(self):
        try:
            cnx = mysql.connector.connect(user='root', password='1100',
                                          host='127.0.0.1', use_unicode=True)
            # auth_plugin='caching_sha2_password')
            return cnx
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                raise Exception(
                    "Something is wrong with your user name or password")
            else:
                raise Exception(f"Error Message from DB: {err}")
        except:
            raise Exception("An error happend connecting to DB.")

    def check_create_db(self):
        cur = self.cur

        # IF THERE IS NO DATABASE BEFORE
        query = ("create database if not exists tweets "
                 "character set utf8mb4 collate utf8mb4_general_ci")
        cur.execute(query)
        cur.execute('use tweets')
        query = """
        create table if not exists tweets_api (
            id int unsigned auto_increment primary key,
            tweet_id varchar(40),
            username varchar(255),
            user_screen_name varchar(255),
            user_id varchar(100),
            tweet varchar(1000),
            location varchar(100),
            searched_hashtag varchar(255),
            created_at varchar(50),
            retweet_count int,
            favorite_count int
        ) character set utf8mb4 collate utf8mb4_general_ci
        """
        cur.execute(query)
        # end of creating DB and table
        self.cnx.commit()

    def check_if_exists(self, tweet_id):
        """
        Checks if the tweet with the given id is already on DB.
        """
        check_if_exists_query = 'select count(1) from tweets_api where tweet_id = %s'
        self.cur.execute(check_if_exists_query, (tweet_id,))
        (already_exists,) = self.cur.fetchone()
        return already_exists > 0

    def insert_tweet(self, tweet_data):
        """
        Inserts the given tweet into the DB.
        """
        insert_tweet_query = (
            'insert into tweets_api (tweet_id, username, user_screen_name, '
            'user_id, tweet, location, searched_hashtag, created_at,'
            'retweet_count, favorite_count) '
            'values (%(tweet_id)s, %(username)s, %(user_screen_name)s, %(user_id)s, '
            '%(tweet)s, %(location)s, %(searched_hashtag)s, %(created_at)s, '
            '%(retweet_count)s, %(favorite_count)s)'
        )
        self.cur.execute(insert_tweet_query, tweet_data)
        self.cnx.commit()

    def get_all_tweets(self, limit=None):
        """
        Returns all the tweets saved in DB.
        """
        self.cur.execute('use tweets')
        if limit is None:
            get_query = "select * from tweets_api"
        else:
            get_query = f"select * from tweets_api order by id desc limit {limit}"
        self.cur.execute(get_query)
        return self.cur.fetchall()

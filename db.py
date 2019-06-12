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
                                          host='127.0.0.1')
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
        cur = self.cnx.cursor()

        # IF THERE IS NO DATABASE BEFORE
        query = ("create database if not exists tweets "
                 "character set utf8mb4 collate utf8mb4_general_ci")
        cur.execute(query)
        cur.execute('use tweets')
        query = """
        create table if not exists tweets (
            id int unsigned auto_increment primary key,
            tweet_id varchar(40),
            user varchar(255),
            tweet varchar(1000),
            tweet_type int,
            hashtag varchar(255),
            timestamp_seconds int,
            tweet_time datetime,
            likes int,
            retweets int,
            replys int
        ) character set utf8mb4 collate utf8mb4_general_ci
        """
        # tweet_type is 0 for tweet and 1 if it's a reply.

        cur.execute(query)
        # end of creating DB and table
        self.cnx.commit()
        cur.close()

    def check_if_exists(self, tweet_id):
        """
        Checks if the tweet with the given id is already on DB.
        """
        check_if_exists_query = 'select count(1) from tweets where tweet_id = %s'
        self.cur.execute(check_if_exists_query, (tweet_id,))
        (already_exists,) = self.cur.fetchone()
        return already_exists > 0

    def insert_tweet(self, tweet_data):
        """
        Inserts the given tweet into the DB.
        """
        insert_tweet_query = (
            'insert into tweets (tweet_id, user, tweet, tweet_type, hashtag, '
            'timestamp_seconds, tweet_time, likes, retweets, replys) '
            'values (%(tweet_id)s, %(user)s, %(tweet)s, %(tweet_type)s, %(hashtag)s, '
            '%(timestamp_seconds)s, %(tweet_time)s, %(likes)s, %(retweets)s, %(replys)s)'
        )
        self.cur.execute(insert_tweet_query, tweet_data)
        self.cnx.commit()

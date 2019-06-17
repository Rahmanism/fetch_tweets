def show_help():
    help_message = """
This app will search for a hashtag and saves the tweets in a MySQL database.

Syntax:
    python gettweets.py [-hg hashtag] [-c nn] [-l lang] [-h|--help] [-x filename.csv [-xc limit]]

-hg hashtag     : is the term you want to search in twitter.
-c  nn          : will fetches (nn) tweets, default is 10.
-h, --help      : will show this help page.
-l lang         : sets the language of search.
-x
   filename.csv : To export what's in DB to a csv file.
                  If you use this switch, the others won't work.
                  Default file name is `tweets.csv` in current directory.
-xc limit       : We can set that how many of latest tweets we want to export to CSV.
                  `limit` is the number!
                  This switch only work if you use the `-x`.
                  Without `-xc` you will have all records exported.

    """
    print(help_message)
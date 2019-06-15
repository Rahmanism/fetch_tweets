def show_help():
    help_message = """
This app will search for a hashtag and saves the tweets in a MySQL database.

Syntax:
    python gettweets.py [-hg hashtag] [-c nn] [-l lang] [-h|--help] [-x filename.csv]

-hg hashtag     : is the term you want to search in twitter.
-c  nn          : will fetches (nn) tweets, default is 10.
-h, --help      : will show this help page.
-l lang         : sets the language of search.
-x
   filename.csv : To export what's in DB to a csv file.
                  If you use this switch, the others won't work.
                  Default file name is `tweets.csv` in current directory.

    """
    print(help_message)
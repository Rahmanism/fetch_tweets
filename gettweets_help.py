def show_help():
    help_message = """
This app will search for a hashtag and saves the tweets in a MySQL database.

Syntax:
    python gettweets.py [hashtag] [-top] [-h|--help]

hashtag    : is the term you want to search in twitter.
-top       : will search the top tweets. Without this option the recent tweets will be used.
-h, --help : will show this help page.
    
    """
    print(help_message)
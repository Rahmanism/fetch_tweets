def show_help():
    help_message = """
This app will search for a hashtag and saves the tweets in a MySQL database.

Syntax:
    python gettweets_api.py [hashtag] [-top] [-h|--help]

hashtag    : is the term you want to search in twitter.
             If you use hashtag in command line it should be the first argument.
-top       : will search the top tweets. Without this option the recent tweets will be used.
-h, --help : will show this help page.
    
    """
    print(help_message)
from os import environ
import sys
import praw
from log import log


def create_reddit():
    try:
        log("Login in to reddit...")
        reddit = praw.Reddit(client_id=environ.get("CLIENT_ID"),
                             client_secret=environ.get("CLIENT_SECRET"),
                             password=environ.get('PASSWORD'),
                             user_agent=environ.get('USERAGENT'),
                             username=environ.get('ACCOUNT_NAME'))
        log("Account: ", reddit.user.me())
        return reddit
    except Exception as e:
        print("Failed reddit login.")
        print(e)
        sys.exit()

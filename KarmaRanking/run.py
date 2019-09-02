import os
from os.path import abspath, join, dirname
import sys
import praw
from urllib import request
from logging import Logger
from reddit import create_reddit
from config import load_config

logger = Logger("karma-log")

season_names = {
    'fall': '10',
    'winter': '01',
    'spring': '04',
    'summer': '07'
}


def setup():
    load_config()
    return create_reddit()


def make_filename_safe(filename):
    keepcharacters = (' ', '.', '_', '-', '[', ']')
    return "".join(c for c in filename if c.isalnum() or c in keepcharacters).rstrip()


def build_filename(title, ext, suffix):
    title = title.lower().split("|")[-1]

    [week, left_bracket, seasonal] = title.partition('[')
    [season, year] = seasonal.rpartition(']')[0].split(" ")

    season_num = season_names[season]
    week_num = week.strip().split(' ')[1].zfill(2)

    filename_pattern = "[%s-%s_%s]_week-%s%s"
    unsafe_name = filename_pattern % (year,
                                      season_num, season, week_num, suffix)

    good_name = make_filename_safe(unsafe_name)
    filename = good_name + "." + ext
    return abspath(join(dirname(__file__), "./downloads", filename))


def do_search(sub, search):
    timeframe = os.environ.get("TIMEFRAME", "all")
    print("Search subreddit with '%s' in timeframe %s" % (search, timeframe))
    for post in sub.search(search, sort="new", time_filter=timeframe):
        is_imgur = "imgur" in post.url
        is_ireddit = "i.redd.it" in post.url
        is_image_post = is_imgur or is_ireddit
        if not is_image_post:
            continue

        if is_ireddit:
            ext = post.url.split(".")[-1]
            filename = build_filename(post.title, ext, "")
            request.urlretrieve(post.url, filename=filename)

        if is_imgur:
            ext = "zip"
            filename = build_filename(post.title, ext, "-and-overview")
            request.urlretrieve("%s/zip" % post.url, filename=filename)


if __name__ == "__main__":
    reddit = setup()
    anime = reddit.subreddit("anime")

    try:
        search = os.environ.get("SEARCH_STRING", "karma ranking")
        do_search(anime, search)

    except praw.exceptions.APIException as e:
        logger.warn(e)
        logger.warn("Rate limit exceeded. Sleeping for 1 minute.")
    except KeyboardInterrupt:
        logger.info("Exiting...")
        sys.exit()
    except Exception as e:
        logger.exception(e)
        logger.error(str(e.__class__.__name__) + ": Exit")
        sys.exit()

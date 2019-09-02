from os import environ
from os.path import abspath, join, dirname
from dotenv import load_dotenv


def load_config():
    dotenv_path = abspath(join(dirname(__file__), '.env'))
    load_dotenv(dotenv_path)

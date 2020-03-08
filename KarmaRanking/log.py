from logging import Logger

logger = Logger("karma-log")


def log(*txt):
    print(*txt, flush=True)

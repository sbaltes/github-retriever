""" Helper functions for HTTP requests. """

from random import randint

import time


def delay_next_request():
    # reduce request frequency to prevent getting blocked
    delay_ms = randint(100, 1000)
    time.sleep(delay_ms / 1000)

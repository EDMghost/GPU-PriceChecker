import random
import time


def human_delay(min_s=1.5, max_s=4.0):
    time.sleep(random.uniform(min_s, max_s))

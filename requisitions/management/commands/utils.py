import random
from datetime import datetime, timedelta, timezone

def random_date():
    now = datetime.now(tz=timezone.utc)
    return now + timedelta(random.uniform(-1, 0) * 100)


def random_timedelta(factor=100):
    return timedelta(random.uniform(0, 1) * factor)


def log(message):
    print(datetime.now().strftime("%d.%b %Y %H:%M:%S"), message)
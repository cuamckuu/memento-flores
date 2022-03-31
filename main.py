import datetime
import random
import time


def get_next_run_time(
    now: datetime.datetime,
    user: str,
    once_per: datetime.timedelta,
    seed: int = 42,
) -> datetime.datetime:
    ts_seconds = int(now.timestamp())
    period_seconds = int(once_per.total_seconds())

    ts_from_seconds = ts_seconds - (ts_seconds % period_seconds)
    random.seed(user + str(seed) + str(ts_from_seconds))

    # Avoid hitting times too close to borders
    stepaway = int(period_seconds * 0.1)
    delta_seconds = random.randint(stepaway, period_seconds-stepaway)

    return datetime.datetime.fromtimestamp(ts_from_seconds + delta_seconds)


if __name__ == '__main__':
    user = 'cuamckuu'
    once_per = datetime.timedelta(minutes=1)
    now = datetime.datetime.utcnow()

    next_run = get_next_run_time(now, user, once_per)

    while True:
        now = datetime.datetime.utcnow()
        if now >= next_run:
            # Some kind of simple deduplication on restart
            delta = (next_run - now).total_seconds()
            if delta < 10:
                print(f'[{now}] Fire reminder!')

            next_run = get_next_run_time(now + once_per, user, once_per)
            print(f'[{now}] Next Run at: {next_run}')
            print()

        time.sleep(2)

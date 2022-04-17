import datetime
from logger import logs
import time

def get_today_datetime():
    return datetime.datetime.now()

def get_datetime_obj(timestamp):
    return datetime.datetime.fromtimestamp(timestamp)

def add_days_to_datetime(date, num_days):
    return date + datetime.timedelta(days=num_days)

def remove_time(date):
    return date.strftime('%Y-%m-%d')

def get_current_day_of_week():
    return datetime.datetime.today().strftime('%A')

def get_today_time_at(hr, min=0, sec=0):
    now = get_today_datetime()
    return now.replace(hour=hr, minute=min, second=sec)    

def wait_for_time_to_be(hr, min=0, sec=0):
    expected_time = get_today_time_at(hr, min, sec)
    logs.info(f"Waiting for time to be {expected_time}")
    while (get_today_datetime() < expected_time):
        time.sleep(1)

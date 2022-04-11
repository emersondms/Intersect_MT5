import datetime

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


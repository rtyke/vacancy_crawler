import datetime
import time
import os

import tzlocal


LOCAL_TZ = tzlocal.get_localzone()


def unixtime_from_datetime(date_to_convert):
    return int(time.mktime(date_to_convert.timetuple()))


def get_unixtime_hours_back(hours=1):
    hours_back = datetime.datetime.today() - datetime.timedelta(hours=hours)
    return unixtime_from_datetime(hours_back)


def get_unixtime_halfhour_back(minutes=30):
    halfhour_back = datetime.datetime.today() - datetime.timedelta(minutes=minutes)
    return unixtime_from_datetime(halfhour_back)


def get_unixtime_several_mins_back(minutes=10):
    halfhour_back = datetime.datetime.today() - datetime.timedelta(minutes=minutes)
    return unixtime_from_datetime(halfhour_back)


def get_unixtime_several_days_back(days=10):
    halfhour_back = datetime.datetime.today() - datetime.timedelta(days=days)
    return unixtime_from_datetime(halfhour_back)


def get_unixtime_month_back(days=30):
    month_back = datetime.datetime.today() - datetime.timedelta(days=days)
    return unixtime_from_datetime(month_back)


def from_str_time_to_unixtime(time_string, string_time_format='%Y-%m-%d %H:%M:%S'):
    """
    Convert string in local time (Mac Os) to seconds since epoch.
    """
    time_converted = datetime.datetime.strptime(time_string, string_time_format)
    seconds = time.mktime(time_converted.timetuple())
    return int(seconds)


def from_unixtime_to_strtime(unixtime, string_time_format='%Y-%m-%d %H:%M:%S'):
    time_local = datetime.datetime.fromtimestamp(unixtime, LOCAL_TZ)
    time_str = time_local.strftime(string_time_format)
    return time_str


def get_current_path():
    return os.path.dirname(os.path.realpath(__file__))
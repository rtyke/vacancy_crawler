import datetime
import time
import os

import tzlocal


LOCAL_TZ = tzlocal.get_localzone()


def isotime_from_unixtime(date_to_convert):
    return datetime.datetime.fromtimestamp(date_to_convert).isoformat()


def isotime_from_datetime(date_to_convert):
    return date_to_convert.isoformat()

def current_isotime():
    return datetime.datetime.now().isoformat()


def get_isotime_several_mins_back(minutes=10):
    several_mins_back = datetime.datetime.today() - datetime.timedelta(minutes=minutes)
    return several_mins_back.isoformat()


def get_isotime_several_days_back(days=10):
    several_days_back = datetime.datetime.today() - datetime.timedelta(days=days)
    return several_days_back.isoformat()


def unixtime_from_datetime(date_to_convert):
    return int(time.mktime(date_to_convert.timetuple()))


def unixtime_from_strtime(time_string, string_time_format='%Y-%m-%d %H:%M:%S'):
    """
    Convert string in local time (Mac Os) to seconds since epoch.
    """
    time_converted = datetime.datetime.strptime(time_string, string_time_format)
    seconds = time.mktime(time_converted.timetuple())
    return int(seconds)


def strtime_from_unixtime(unixtime, string_time_format='%Y-%m-%d %H:%M:%S'):
    time_local = datetime.datetime.fromtimestamp(int(unixtime), LOCAL_TZ)
    time_str = time_local.strftime(string_time_format)
    return time_str


def get_unixtime_several_mins_back(minutes=10):
    several_mins_back = datetime.datetime.today() - datetime.timedelta(minutes=minutes)
    return unixtime_from_datetime(several_mins_back)


def get_unixtime_hours_back(hours=1):
    hours_back = datetime.datetime.today() - datetime.timedelta(hours=hours)
    return unixtime_from_datetime(hours_back)


def get_unixtime_several_days_back(days=10):
    several_days_back = datetime.datetime.today() - datetime.timedelta(days=days)
    return unixtime_from_datetime(several_days_back)


def get_current_path():
    return os.path.dirname(os.path.realpath(__file__))
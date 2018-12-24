import datetime
import time
import os


def unixtime_from_datetime(date_to_convert):
    return int(time.mktime(date_to_convert.timetuple()))


def get_unixtime_halfhour_back():
    halfhour_back = datetime.datetime.today() - datetime.timedelta(minutes=10)
    return unixtime_from_datetime(halfhour_back)


def get_unixtime_month_back():
    month_back = datetime.datetime.today() - datetime.timedelta(days=10)
    return unixtime_from_datetime(month_back)


def get_current_path():
    return os.path.dirname(os.path.realpath(__file__))


def from_str_time_to_unixtime(time_string, string_time_format):
    """
    time_string = "01/12/2011 14:00:01"
    string_time_format = "%d/%m/%Y %H:%M:%S"

    """
    import time
    import datetime
    res = time.mktime(datetime.datetime.strptime(time_string, string_time_format).timetuple())
    return res


def from_unixtime_to_datetime(unixtime):
    from datetime import datetime
    dt = datetime.utcfromtimestamp(unixtime).strftime('%Y-%m-%d %H:%M:%S')
    return dt
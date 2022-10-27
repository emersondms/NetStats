import datetime
import calendar

def get_today_datetime():
    return datetime.datetime.now() 

def get_day_number(datetime_obj):
    return int(datetime_obj.strftime('%d'))

def get_today_day():
    return get_day_number(get_today_datetime())

def get_last_day_of_current_month():
    today_datetime  = get_today_datetime()
    last_datetime_of_current_month = today_datetime.replace(
        day = calendar.monthrange(today_datetime.year, today_datetime.month)[1])
    return get_day_number(last_datetime_of_current_month)

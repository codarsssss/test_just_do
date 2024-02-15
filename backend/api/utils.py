def datatime_to_start_day(datetime):
    return datetime.replace(hour=0, minute=0, second=0)


def datetime_to_end_day(datetime):
    return datetime.replace(hour=23, minute=59, second=59)

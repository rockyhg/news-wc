from datetime import datetime, timedelta


def jp_time_now():
    return datetime.utcnow() + timedelta(hours=9)


def jp_today():
    return jp_time_now().date()

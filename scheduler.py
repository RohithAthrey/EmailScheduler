from datetime import datetime, timezone, timedelta
def calculate_send_time(time: datetime):
    day = datetime(time.year, time.month, time.day, 16, 1, 0) 
    day_of_week = time.weekday()
    if (day_of_week == 5 or day_of_week == 6 or (day_of_week == 4 and time > day)):
        days_until_monday = (7 - day_of_week) % 7
        if days_until_monday == 0:
            days_until_monday = 7
        next_monday = time + timedelta(days=days_until_monday)
        return datetime(next_monday.year, next_monday.month, next_monday.day, 9, 30, 0)
    elif (time > day): 
        next_day = time + timedelta(days=1)
        return datetime(next_day.year, next_day.month, next_day.day, 9, 30, 0)
    elif (time<datetime(time.year, time.month, time.day, 9, 30, 0) ) :
        return datetime(time.year, time.month, time.day, 9, 30, 0)
    else:
        return time
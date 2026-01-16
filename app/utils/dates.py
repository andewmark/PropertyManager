from datetime import date

def current_month_bounds():
    today = date.today()
    first_day = today.replace(day=1)

    if today.month == 12:
        next_month = today.replace(year=today.year + 1, month=1, day=1)
    else:
        next_month = today.replace(month=today.month + 1, day=1)

    return today, first_day, next_month
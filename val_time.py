from datetime import datetime


def validate_time(t):
    try:
        datetime.strptime(t, '%H:%M:%S')
        return True

    except ValueError:
        return False


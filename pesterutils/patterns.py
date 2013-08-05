"""
2013 Paul Logston

A collection of pattern definitions with the same call signature and return
signature. All functions take a list of previous successful pestering attempts
and return a datetime of when the next pestering attempt is due.
"""

from datetime import timedelta

def next_fibonacci(j):
    n0, n1 = 1, 1
    cntr = 0
    while cntr < j:
        n0, n1 = n1, n0+n1
        cntr += 1
    return n0;

def every_5_min(pestering_attempts):
    return pestering_attempts[0].attempt_time+timedelta(minutes=5)

def every_10_min(pestering_attempts):
    return pestering_attempts[0].attempt_time+timedelta(minutes=10)

def every_30_min(pestering_attempts):
    return pestering_attempts[0].attempt_time+timedelta(minutes=30)

def every_1_hr(pestering_attempts):
    return pestering_attempts[0].attempt_time+timedelta(hours=1)

def every_2_hr(pestering_attempts):
    return pestering_attempts[0].attempt_time+timedelta(hours=2)

def every_4_hr(pestering_attempts):
    return pestering_attempts[0].attempt_time+timedelta(hours=4)

def every_8_hr(pestering_attempts):
    return pestering_attempts[0].attempt_time+timedelta(hours=8)

def every_16_hr(pestering_attempts):
    return pestering_attempts[0].attempt_time+timedelta(hours=16)

def every_1_day(pestering_attempts):
    return pestering_attempts[0].attempt_time+timedelta(days=1)

def fibonacci_min(pestering_attempts):
    interval = next_fibonacci(len(pestering_attempts))
    return pestering_attempts[0].attempt_time+timedelta(minutes=interval)

def fibonacci_day(pestering_attempts):
    interval = next_fibonacci(len(pestering_attempts))
    return pestering_attempts[0].attempt_time+timedelta(days=interval)

def never(pestering_attempts):
    return pestering_attempts[0].attempt_time+timedelta(years=100)

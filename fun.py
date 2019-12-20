import time
import datetime
from datetime import timedelta
from dateutil.parser import parse

def Convert(date):
    dt = parse(date)
    dt = dt + timedelta(hours=3)
    times =dt.strftime("%b %d %Y %H:%M:%S")
    return times
    

def Convert4User(date):
    dt = parse(date)
    dt = dt + timedelta(hours=3)
    times =dt.strftime("%b %d - %Y at %H :%M:%S")
    return times

def TimeJoke():
    t = time.time()
    print(t)


# TimeJoke()

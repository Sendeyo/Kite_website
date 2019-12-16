import time
import datetime
from datetime import timedelta
from dateutil.parser import parse

def Convert(date):
    dt = parse(date)
    dt + timedelta(hours=9)
    times =dt.strftime("%b %d %Y %H:%M:%S")
    return times

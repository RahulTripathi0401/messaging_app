''' General helpful functions '''
import datetime
import re
from threading import Timer
import server

def emailCheck(email):
    ''' Regex for checking if an email is valid '''
    regex = r'^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
    return bool(re.search(regex, email))


timers = []
def clearDatabase():
    ''' Clearing data for pytesting '''
    server.users.clear()
    server.channels.clear()
    timers.clear()

time_now = None

def get_time():
    ''' return current time '''
    global time_now
    if time_now is not None:
        return time_now
    return datetime.datetime.now()

def set_time(time_to_set):
    ''' set current time '''
    global time_now
    time_now = time_to_set
    for timer in timers:
        if timer.end <= time_now:
            timer.function(*timer.args)
            timers.remove(timer)

def run_later(interval, function, args):
    ''' run a function later '''
    global time_now
    timer = Timer(interval, function, args)
    if time_now is None:
        timer.start()
    else:
        timer.end = time_now + datetime.timedelta(seconds=interval)
        timers.append(timer)

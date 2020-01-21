# -*- coding: utf-8 -*-

import time
import utilParse
from datetime import datetime


class StopWatch:
    def __init__(self):
        self.time = time.time()
        self.Lap = 0
    def stop(self):
        return time.time() - self.time
    def getLapTimeString(self, roundTo):
        timeString = ""
        if self.Lap == 0:
            timeString = str(round(time.time() - self.time,roundTo)) + " seconds"
        else:
            timeString = str(round(time.time() - self.Lap,roundTo)) + " seconds"
        self.Lap = time.time()
        return timeString
    def getFullTimeString(self,roundTo):
        return str(round(time.time() - self.time,roundTo)) + " seconds"
    
def timeToDateString(timestamp):
    o = datetime.fromtimestamp(timestamp)
    time = str(o.time())
    delimiter = utilParse.findCharacter(time,".")
    if delimiter == -1:
        return str(o.date()) + " " + str(o.time())
    return str(o.date()) + " " + str(time[0:delimiter])

def getDateString():
    return timeToDateString(time.time())

"""
s = StopWatch()
time.sleep(0.25)
print(s.getLapTimeString(4))
time.sleep(0.5)
print(s.getLapTimeString(4))
print(s.getFullTimeString(4))
"""
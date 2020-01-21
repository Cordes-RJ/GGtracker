# -*- coding: utf-8 -*-

import requests
import utilTime
import time

# a request func
def getResponseText(URL,headerTxt, timeout):
    headers = {"User-Agent": headerTxt}
    return requests.get(URL, headers=headers, timeout=timeout).text

def politelyScrape(objectList,URLbuildFunc, requestFunc, parseResponseFunc,headerTxt,timeout):
    parsed = []
    for i in objectList:
        url = URLbuildFunc(i)
        responseText = ""
        stopwatch = utilTime.StopWatch()
        responseText = requestFunc(url,headerTxt,timeout)
        t = stopwatch.stop()
        if responseText != "":
            parsed.append(parseResponseFunc(responseText))
        time.sleep(int(t * 1.1)) # being polite to server
        # we give the server 10% more time then it takes to respond
    return parsed
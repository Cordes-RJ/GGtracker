# -*- coding: utf-8 -*-

"""
ironforge.py provides functions to scrape and update ironforge.ru
"""

from selenium import webdriver
#from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.errorhandler import UnexpectedAlertPresentException
import time
import logger

#buildURL creates a URL from a name and a server
def buildURL(name,server):
    return "https://ironforge.pro/?player="+name+"-"+server

# Update updates all characters in the given list
def buildDriver(driverPath,headless):
   try:
       opt = webdriver.firefox.options.Options()
       opt.headless= headless 
       return webdriver.Firefox(options=opt,executable_path = driverPath)
   except:
       errmsg = "Failed to build driver, check that geckodriver.exe is installed at the driverPath location"
       logger.Log("ironforge","buildDriver","Critical",errmsg,LogAndKill=True)

def scrapeCharacter(driver,character,server,attemptLimit, waitTime):
    driver.get(buildURL(character,server))
    y = scrapeAttempt(driver,0, attemptLimit,waitTime)
    gear = []
    for item in y:
        gear.append(item.text)
    return gear
    
def scrapeAttempt(driver,attemptCt, attemptLimit,waitTime):
    if attemptCt >= attemptLimit:
        return []
    #else
    driver.implicitly_wait(waitTime)
    try:
        y = driver.find_elements_by_tag_name("h5")
        if type(y) != list:
            return scrapeAttempt(driver,attemptCt+1,attemptLimit,waitTime)
        elif len(y) == 0:
            return scrapeAttempt(driver,attemptCt+1,attemptLimit,waitTime)
        else:
            return y
    except:
        return []
    
def Scrape(characterList,server,attemptLimit,waitTime,headless,path):
    driver = buildDriver(path,headless)
    gear = {}
    for character in characterList:
        gear[character] = scrapeCharacter(driver,character,server,attemptLimit,waitTime)
        time.sleep(waitTime)
    driver.close()
    return gear

def updateChar(driver,character,server,attemptLimit, waitTime):
    # this is hacky, but hacky websites call for hacky measures.
    # the site only throws a second alert 30% of the time, and half of
    # those times selenium isn't picking it up as an alert?
    # so instead, it's gonna just try to move past a previous pages alert
    # 4 separate times just incase the site loads the alert slowly
    try:
        driver.get(buildURL(character,server))
    except UnexpectedAlertPresentException:
        try:
            driver.get(buildURL(character,server))
        except UnexpectedAlertPresentException:
            try:
                driver.get(buildURL(character,server))
            except UnexpectedAlertPresentException:
                driver.get(buildURL(character,server))
    updateAttempt(driver,0, attemptLimit,waitTime)
    
def updateAttempt(driver,attemptCt, attemptLimit,waitTime):
    if attemptCt >= attemptLimit:
        return []
    #else
    driver.implicitly_wait(waitTime)
    try:
        try:
            y = driver.find_element_by_class_name("update-character-button")
            y.click()
            time.wait(4)
        except UnexpectedAlertPresentException:
            pass
    except:
        updateAttempt(driver,attemptCt+1, attemptLimit,waitTime)
    
def Update(characterList,server,attemptLimit,waitTime,headless,path):
    driver = buildDriver(path,headless)
    for character in characterList:
        updateChar(driver, character, server, attemptLimit,waitTime)
        time.sleep(waitTime)
    driver.close()
        
"""
charList = ["hanham","Wambamtymam","Shrekk","Jarlragnaar","Tyrona"]
path = 'C://Users//XYZ//Anaconda3//Lib//site-packages//selenium//webdriver//firefox//geckodriver-v0.26.0-win64//geckodriver.exe'
Update(charList,"Kirtonos",2,1,False,path)
"""
# -*- coding: utf-8 -*-

"""
logger makes logs in a readable, csv format for scripting projects. 
example usage:
    
# with default local log file
logger.Start()

# with custom log file
logger.Start(LogPath = "directoryOfChoice/file.csv")
logger.Log("Package","Function","Note|Warning|Critical","Memo")
Logger.Log("logger","Examples","Critical","Something is terribly wrong", LogAndKill = True)
# LogAndKill will exit the program
"""



import utilFile
import sys
import time

global LogPath
LogPath = "log.csv"

# reset/set log
def Start(**kwargs):
    note = False # if custom log fails to be created, set to true
    if "LogPath" in kwargs.keys():  # if a logpath was given
        if setNewLogFileAt(kwargs['LogPath']): # try to create given log file
            # if successful, return, else continue
            return 
        else:
            note = True # note that custom log failed to init
    # settle for standard local log
    if setNewLogFileAt('log.csv'):
        if note: # if note is set to True, log warning about custom log failure  
            Log("logger","Start","Warning","Custom log failed to init-logging in local logcsv")
        return
    else:
        # was unable to create file in local directory
        print("GBank failed to create local log. Check logger.py")
        sys.exit() # exit
            
# set new log file at given path        
def setNewLogFileAt(path):
    try:
        if utilFile.Exists(path): # if the file exists
            utilFile.Erase(path) # erase contents
        else: # if file doesn't exist
            utilFile.Create(path) # create it
        # check if default log exists, and erase it to avoid confusion
        global LogPath # global call
        if utilFile.Exists(LogPath):
            utilFile.Erase(LogPath)
        # Now set new default logpath
        LogPath = path # reset Global Var
        createLogHeader()
        return True # success
    except Exception:
        return False # failure
    
# returns log string
def makeLogString(Package, Function, LogType, ContentString):
    return ("%s,%s,%s,%s,%s" % (time.time(), Package, Function, LogType, ContentString))

def createLogHeader():
    logString = "Time,Package,Function,LogType,Memo"
    try:
        with open(LogPath, "a+") as IntoLog:
            IntoLog.write(logString + "\n")
            IntoLog.close()
    except Exception:
        # was unable to write to log
        print("GBank failed to write to log header. Check logger.py")
        sys.exit() # exit

# log will log data to log.csv, with option "LogAndKill" == True to exit
# and write to console to inform the user to check logs
def Log(Package, Function, LogType, ContentString, **kwargs):
    logString = makeLogString(Package, Function, LogType, ContentString)
    try:
        with open(LogPath, "a+") as IntoLog:
            IntoLog.write(logString + "\n")
            IntoLog.close()
        if 'LogAndKill' in kwargs.keys():
            if kwargs['LogAndKill'] == True:
                print("GBank Notice: Check Logfile...\n %s" % logString)
                sys.exit()
    except Exception:
        # was unable to write to log
        print("GBank failed to write to log. Check logger.py")
        sys.exit() # exit
            

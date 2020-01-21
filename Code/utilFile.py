# -*- coding: utf-8 -*-

import os

# checks if file exists, returns a bool
def Exists(path): # string -> bool
    return os.path.isfile(path)

# erases contents at path
def Erase(path):
    if Exists(path):
        open(path, 'w').close()
        
def Create(path):
    open(path, 'a').close()

# read file in as a block
def ReadIn_lines(path):
    Lines = []
    try:
        with open(path, "r",encoding = "utf8") as File:
            Lines = File.readlines()
            File.close()
    except:
        pass
    return Lines

# read in file as bloc of text
def ReadIn_asBloc(path):
    string = []
    try:
        with open(path, "r",encoding = "utf8") as File:
            string = File.read()
            File.close()
    except:
        pass
    return string
    
def ListOfItemsToCSVRow(List):
    csvString = ""
    for i in List:
        csvString += "," + str(i)
    return csvString[1:len(csvString)]

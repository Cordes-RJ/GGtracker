# -*- coding: utf-8 -*-

import pandas as pd
import utilMap
import utilFile
import logger
import wowhead


class Item:
    def __init__(self):
        self.itemID = 0
        self.new = True
        self.Name = ""
        self.Rarity = -1
        self.IconName = ""
        self.Slot = ""
    def INITviaDFrow(self,dfRow):
        self.itemID = dfRow['itemID']
        self.Name = (dfRow['Name'])
        self.Rarity = dfRow['Rarity']
        self.IconName = (dfRow['IconName'])
        self.Slot = dfRow['Slot']
        self.new = False # was found in a previous update
        return self
    def ToCSVrow(self):
        name = self.Name
        iconName = self.IconName
        link = wowhead.makeDisplayURLfromItemID(self.itemID)
        attList = [name,self.itemID,self.Rarity,iconName,self.Slot,link]
        return utilFile.ListOfItemsToCSVRow(attList)
    def INITviaID(self, itemID):
        self.itemID = itemID
        return self
    def UpdateWoWheadInfo(self, winfo):
        self.Name = (winfo.Name)
        self.itemID = winfo.itemID
        self.Rarity = winfo.Rarity
        self.Slot = winfo.InventorySlot
        self.IconName = (winfo.IconName)        

# take raw CSV path and return Pandas dataframe
# assumes header
def getFileContents(path):
    Lines =pd.read_csv(path)
    if len(Lines) <= 0:
        # for readability
        errMessage = "Error getting itemRef file|check parameters and itemref folder"
        logger.Log("warehouse","getFileContent","Critical", errMessage, LogAndKill = True)
        # exit program
    # clean the ropes of unneccessary control chars
    return Lines

def dfRowToAttributeList(dfRow):
    attributeStrings = ['itemID','Name','Link','Rarity','IconName','Type','Subtype','LastPrice','Ct']
    itemRow = []
    for attribute in attributeStrings:
        itemRow.append(dfRow[attribute])
    return itemRow
    
# returns dictionary of items 
def Build(Path):
    df = getFileContents(Path)
    items = []
    for i,i2 in df.iterrows():
        items.append(Item().INITviaDFrow(i2))
    itemDict = utilMap.Map(-1)
    for item in items:
        itemDict.Add(item.itemID,item)
    return itemDict
        





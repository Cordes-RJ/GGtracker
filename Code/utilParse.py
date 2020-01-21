# -*- coding: utf-8 -*-

# removes control characters from a string
def removeControlCharacters(string):
    bytesArray = convertToBytes(string)
    newString = ""
    for i in range(len(bytesArray)):
        if bytesArray[i] >= 32:
            newString = newString+string[i]
    return newString

def removeControlCharactersFromList(List):
    newList = []
    for item in List:
        newList.append(removeControlCharacters(str(item)))
    return newList

# count characters in a string, preferred input is character as string
# int representation of a byte will not work
def countCharacters(string, char):
    if len(char) == 0:
        return -1
    if len(char) > 1:
        return countSubStrings(string, char)
    count = 0
    bytesArray, byteChar = convertToBytes(string), convertToBytes(char)[0]
    for i in range(len(bytesArray)):
        if bytesArray[i] == byteChar:
            count += 1
    return count

# convert pretty much anything to byte array
def convertToBytes(anything):
    if type(anything) == type("xy".encode('utf-8')):
        return anything
    else:
        return str(anything).encode('utf-8')

class Error(Exception):
    pass

# used in byte search
class NotCharacter(Error):
    pass

def findCharacter(string, char, **kwargs):
    if len(string) < len(char):
        return -1
    if len(string) == 0 or len(char) == 0:
        return -1
    start = 0
    end = len(string)
    # handle kwargs
    if "startIndexAt" in kwargs.keys():
        start = kwargs["startIndexAt"]
    if "endIndexAt" in kwargs.keys():
        end = kwargs["endIndexAt"]
    if len(char)>1:
        return findSubstring(string,char,startIndexAt=start,endIndexAt=end)
    # convert bytes
    bytesArray, byteChar = convertToBytes(string), convertToBytes(char)[0]
    for i in range(start,end):
        if bytesArray[i] == byteChar:
            return i
    return -1

# find substring within a larger string
# specify start and end range with startIndexAt and endIndexAt
def findSubstring(string, substring, **kwargs):
    if len(string) < len(substring):
        return -1
    if len(string) == 0 or len(substring) == 0:
        return -1
    start = 0
    end = len(string)
    # handle kwargs
    if "startIndexAt" in kwargs.keys():
        start = kwargs["startIndexAt"]
    if "endIndexAt" in kwargs.keys():
        end = kwargs["endIndexAt"]
    # if substring is a single character, use findChar instead
    if len(substring) == 1:
        return findCharacter(string, substring, startIndexAt=start,endIndexAt=end)
    # update end to account for subtring length
    end -= (len(substring)-1)
    if end < start:
        return -1
    bytesArray, bytesSubArray = convertToBytes(string), convertToBytes(substring)
    for i in range(start, end):
        if bytesArray[i] == bytesSubArray[0]:
            found = True
            for i2 in range(i+1,i+len(bytesSubArray)):
                if bytesArray[i2] != bytesSubArray[(i2-i)]:
                    found = False
                    break
            if found:
                return i
    return -1

# findStrangeDatum pulls data from within odd delimiters in text data
# if it finds nothing, it will return "", else it will return the datum found
# within the delimiters
# i.e. <test!>the Datum we Want</test!>
def findStrangeDatum(string,startDelimit,endDelimit, **kwargs):
    if len(string) < len(endDelimit) + len(startDelimit):
        return ""
    if len(string) == 0 or len(startDelimit) == 0 or len(endDelimit) == 0:
        return ""
    start = 0
    end = len(string)
    if "startIndexAt" in kwargs.keys():
        start = kwargs["startIndexAt"]
    if "endIndexAt" in kwargs.keys():
        end = kwargs["endIndexAt"]
    # find where starting delimiter begins
    a = findSubstring(string,startDelimit,startIndexAt=start,endIndexAt=end)
    if a == -1:
        return ""
    a += len(startDelimit)
    if end < a:
        return ""
    b = findSubstring(string,endDelimit,startIndexAt=a,endIndexAt=end)
    if b == -1:
        return ""
    return string[a:b]

def findAllCharacters(string,char, **kwargs):
    if len(string) < len(char):
        return ""
    if len(string) == 0 or len(char) == 0:
        return ""
    if len(char) > 1:
        return findAllSubstrings(string, char)
    start = 0
    end = len(string)
    if "startIndexAt" in kwargs.keys():
        start = kwargs["startIndexAt"]
    if "endIndexAt" in kwargs.keys():
        end = kwargs["endIndexAt"]
    foundList = []
    bytesArray, byteChar = convertToBytes(string), convertToBytes(char)[0]
    for i in range(start,end):
        if bytesArray[i] == byteChar:
            foundList.append(i)
    return foundList
            
    

def findAllSubstrings(string, substring, **kwargs):
    if len(string) < len(substring):
        return ""
    if len(string) == 0 or len(substring) == 0:
        return ""
    start = 0
    end = len(string)
    overlap = False
    if "startIndexAt" in kwargs.keys():
        start = kwargs["startIndexAt"]
    if "endIndexAt" in kwargs.keys():
        end = kwargs["endIndexAt"]
    if "overlap" in kwargs.keys():
        overlap = kwargs["overlap"]
    x = True
    foundList = []
    # if we don't want overlap in substring discovery, i.e.:
        # searching for "ABCA" in "ABCABCA"
            # with overlap: we'll return a count of 2, |ABCA|BCA and then BC|ABCA
            # without, we'll return a count of 1, |ABCA|BCA ... BCA
    if overlap:
        increment = lambda x: x + 1
    else:
        increment = lambda x: x + len(substring)
    while x:
        foundAt = findSubstring(string, substring,startIndexAt=start,endIndexAt=end)
        if foundAt != -1:
            foundList.append(foundAt)
            start = increment(foundAt)
        else:
            x = False
    return foundList

def countSubStrings(string, substring, **kwargs):
    if len(string) < len(substring):
        return -1
    if len(string) == 0 or len(substring) == 0:
        return -1
    start = 0
    end = len(string)
    overlap = False
    if "startIndexAt" in kwargs.keys():
        start = kwargs["startIndexAt"]
    if "endIndexAt" in kwargs.keys():
        end = kwargs["endIndexAt"]
    if "overlap" in kwargs.keys():
        overlap = kwargs["overlap"]
    if len(substring) == 1:
        return countCharacters(string, substring,startIndexAt=start,endIndexAt=end)
    x = True
    foundCt = 0
    # if we don't want overlap in substring discovery, i.e.:
        # searching for "ABCA" in "ABCABCA"
            # with overlap: we'll return a count of 2, |ABCA|BCA and then BC|ABCA
            # without, we'll return a count of 1, |ABCA|BCA ... BCA
    if overlap:
        increment = lambda x: x + 1
    else:
        increment = lambda x: x + len(substring)
    while x:
        foundAt = findSubstring(string, substring,startIndexAt=start,endIndexAt=end)
        if foundAt != -1:
            foundCt += 1
            start = increment(foundAt)
        else:
            x = False
    return foundCt

def DeepCopyList(List):
    NewList = []
    for i in List:
        NewList.append(i)
    return NewList

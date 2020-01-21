# -*- coding: utf-8 -*-
"""
utilMap adds decorators for dictionary that allows for readability and
reduced code replication
"""


class Map:
    def __init__(self, defaultReturn):
        self.m = dict()
        self.default = defaultReturn # what is returned in a failure to get key
    def ListKeys(self):
        return self.m.keys()
    def InMap(self,key):
        if key in self.m.keys():
            return True
        return False
    def Set(self, key, value):
        self.m[key] = value
    def Add(self, key, value):
        self.m[key] = value
    def Del(self,key):
        if self.InMap(key):
            self.m.pop(key)
    # set the default return to be used for now on
    def setDefaultReturn(self,defaultReturn):
        self.default = defaultReturn
    # 
    def Get(self,key):
        if self.InMap(key):
            return self.m[key]
        return self.default
    def DeepCopy(self):
        m = Map(self.default)
        List = self.ListKeys()
        for key in List:
            m.Add(key,self.Get(key))
        return m
    def ReverseLookupOne(self, value):
        for key in self.ListKeys():
            if type(self.m[key]) == type(value):
                if self.m[key] == value:
                    return key
                
class TwoWayMap:
    def __init__(self, defForward, defBack):
        self.forward = Map(defForward)
        self.back = Map(defBack)
    def orient(self,direction):
        if direction:
            return self.forward
        return self.back
    def ListKeys(self,direction):
        return self.orient(direction).ListKeys()
    def InMap(self,direction, key):
        return self.orient(direction).InMap(key)
    def Set(self,direction,key, val):
        k, v = key, val
        if not direction:
            k, v = val, key # reverse
        self.forward.Set(k,v)
        self.back.Set(v,k)
    def Add(self,direction,key, val):
        self.Set(direction, key, val)
    def Del(self,direction,key):
        self.orient(direction).Del(key)
    def setDefaultReturn(self,direction,defaultReturn):
        self.orient(direction).setDefaultReturn(defaultReturn)
    def Get(self,direction,key):
        return self.orient(direction).Get(key)
    def DeepCopy(self):
        newMap = TwoWayMap(self.defaultReturn)
        newMap.forward = self.forward.DeepCopy()
        newMap.back = self.back.DeepCopy()
        return newMap          

def CreateMapofEmptyInterfaces(ListOfKeys):
    m = Map("")
    for key in ListOfKeys:
        m.Add(key,EmptyInterface())
    return m
    
# wanted something similar to an empty interface obj in go
def EmptyInterface():
    return type('', (), {})()
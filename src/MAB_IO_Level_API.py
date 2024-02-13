#Level API
#version 1.1

class Level():
    """  this class represents the level in which the player evolve """

    def __init__(self):
        self.dimX = 100
        self.dimY = 25
        #dimmension of the section of model space allowed and used for the level

        self.gameObjects = {}





def levelInitiate():
    return Level()

def levelAddGameObject(level,key,gameObject):
    if key in level.gameObjects:
        level.gameObjects[key].append(gameObject)
        return len(level.gameObjects[key])-1
    else:
        level.gameObjects[key] = [gameObject]
        return 0

def levelGetGOsByKey(level,key):
    return [ GO for GO in level.gameObjects[key] if GO.alive ] 

def levelGetGOsByKeys(level,keyList):
    ret = []
    for key in keyList:
        ret = ret + levelGetGOsByKey(level,key)
    return ret

def levelGetAllGOs(level):
    ret = []
    for key in level.gameObjects:
        ret = ret + levelGetGOsByKey(level,key)
    return ret

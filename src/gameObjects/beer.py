from elements.IGRectElem import RectElem
from elements.commonRect import rectElemBindImage
from elements.IGRectElem import checkProximity
from gameObjects.GameObject import killGO

from camera import loadImageAsAsset

class Beer():
    """ beer that the player can collect """
    def __init__(self,position):
        self.label = "Beer"
        self.alive = True
        self.elem = RectElem(position,1,1,(0,255,0))
        rectElemBindImage(self.elem,"beer")

def beerLoadContent(texture,camera):
    """ Loads content in palette for Beer GO"""

    path =  r".\noncolliders_sprite\beer.png"
    loadImageAsAsset(texture,camera,"beer",(1,1),path,colorKey = (255,0,255))
    #loading base image

def beerUpdate(beer,player):
    if checkProximity(player.elem,beer.elem,(0,0,0,0)):
        killGO(beer)
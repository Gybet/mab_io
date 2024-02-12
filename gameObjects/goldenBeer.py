from gameObjects.GameObject import killGO
from gameObjects.GameObject import gameObjectListGetElemList
from gameObjects.GameObject import playerPowerUp
from gameObjects.elements.element import RectElem
from gameObjects.elements.element import rectElemBindImage
from gameObjects.elements.element import checkProximity
from gameObjects.elements.element import rectElemEnableDynamics
from gameObjects.elements.element import rectElemCheckLanded
from gameObjects.elements.element import rectElemDynamicalUpdate
from gameObjects.camera.MAB_IO_Camera import loadImageAsAsset

import pygame
vec = pygame.Vector2


class GoldenBeer():
    """ beer that the player can collect """
    def __init__(self,position,powerUpSound):
        self.label = "GoldenBeer"
        self.alive = True
        self.elem = RectElem(position,1,1,(0,255,0))
        self.powerUpSound = powerUpSound
        rectElemEnableDynamics(self.elem,1)
        rectElemBindImage(self.elem,"goldenBeer")

def goldenBeerLoadContent(texture,camera):
    """ Loads content in palette for Beer GO"""

    path =  r".\noncolliders_sprite\goldenBeer.png"
    loadImageAsAsset(texture,camera,"goldenBeer",(1,1),path,colorKey = (255,0,255))
    #loading base image

def goldenBeerUpdate(beer,player,dt,GOColliderlist):
    colElemList = gameObjectListGetElemList(GOColliderlist)
    #creation of inputs for Dynamical update - List of colliders
    magnitude = 0
    if rectElemCheckLanded(beer.elem,colElemList):
        magnitude = 25
    collisionDescriptor = rectElemDynamicalUpdate(beer.elem,dt,colElemList,vec(magnitude,0))
    if checkProximity(player.elem,beer.elem,(0,0,0,0)):
        beer.powerUpSound.play()
        playerPowerUp(player)
        killGO(beer)
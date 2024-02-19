from elements.IGRectElem import RectElem
from elements.IGRectElem import rectElemEnableDynamics
from elements.IGRectElem import rectElemDynamicalUpdate
from gameObjects import gameObjectListGetElemList
from pygame import Vector2 as vec

class Enemy:
    def __init__(self,position):
        self.label = "Enemy"
        self.alive = True
        self.elem = RectElem(position,1,1,(0,255,0))
        rectElemEnableDynamics(self.elem,1)

        self.startingPos = position
        self.mvtRange = 5
        self.prevDir = 1


def enemyUpdate(enemy,dt,GOColliderlist):
    colElemList = gameObjectListGetElemList(GOColliderlist)

    dir = enemy.prevDir
    if enemy.elem.pos.x > enemy.startingPos.x + enemy.mvtRange:
        dir = -1
    elif enemy.elem.pos.x < enemy.startingPos.x - enemy.mvtRange:
        dir = 1


    rectElemDynamicalUpdate(enemy.elem,dt,colElemList,vec(10*dir,0))

    enemy.prevDir = dir

def enemyLoadContent(enemy):
    pass

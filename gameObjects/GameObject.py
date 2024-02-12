#Game Object Module
#version 1.1

 

from MAB_IO_Level_API import *
from MAB_IO_Texture_API import *
from gameObjects.elements.element import *
from gameObjects.camera.MAB_IO_Camera import *




"""
DESCRIPTION OF GAME OBJECT INTERFACE

each game object exposes the following property/ field :

.label => string indicating the name of the game object
.elem => element to which the game object is linked
.alive => boolean indicating if the game object used in game or not
functions : 
"""


"""================ GENERAL FUNCTIONS ================="""

def gameObjectListGetElemList(GOList):
    return [go.elem for go in GOList]

def gameObjectRender(GO,screen,camera,texture,showHitBox):
    rectElemRender(GO.elem,screen,camera,texture,showHitBox)

def gameObjectListRender(GOList,screen,camera,texture,showHitBox):
    for GO in GOList :
        gameObjectRender(GO,screen,camera,texture,showHitBox)

def killGO(GO):
    """ deactivates a game object, deactivated game object are not rendered nor updated and cannot be interracted with"""
    GO.alive = False

def resurectGO(GO):
    """reactivates a GO which has been deactivated"""
    GO.alive = True

def GOSetPosition(GO,position):
    GO.elem.pos = position

def GORenderInit():
    pygame.init()

    ratio = 36
    # ratio of pxl/meter (meter in game model)
    camera = Camera( ratio ,25 ,15 )
    camera.pos = vec(0,0)

    WIDTH = int(camera.viewWidth * camera.model2ScreenRatio)
    HEIGHT = int(camera.viewHeight * camera.model2ScreenRatio)

    font = pygame.font.Font(None, 16)
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    #init of camera used to render game objects

    texture = Texture()

    backgroundPath  =  r".\background.png"
    loadImageAsAsset(texture,camera,"background",(25,15),backgroundPath)
    return camera,texture,screen

def drawBackground(screen,texture,camera):
    rect = Rect(0,0,camera.screenWidth,camera.screenHeight)
    screen.blit(texture.palette["background"],rect)

def generalUpdate(camera):
    """ updates general context used to render game objects"""




""" ================================ PLAYER OBJECT ====================================="""






    

       




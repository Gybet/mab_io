#Game Object Module
#version 1.1
#test
from  MAB_IO_Physics import * 
from  MAB_IO_Render import *
from MAB_IO_Level_API import *
from MAB_IO_Texture_API import *
from MAB_IO_Element import *
from MAB_IO_Camera import *

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

class RectPlayer():
    """ Class used to contain player's data when modeled as a rectangle which can move in 2 axis, no rotation allowed"""
    def __init__(self,position,texture,jumpSound):
        self.label = "Player"
        self.alive = True
        playerSize = (1.5,2.5)
        mass = 1
        self.phase = "lean"
        #phases for player are lean , trans, fat
        self.jumpSound = jumpSound
        self.elem = RectElem(position,playerSize[0],playerSize[1],(0,255,0))
        rectElemEnableDynamics(self.elem,mass)
        rectElemBindImage(self.elem,"playerLean")
        #creating the rectElem associated to the rectPlayer gameObject

        self.animationIndexLean  = loadAnimationAsAsset(texture,"playerAnimLean",0.2,nbMaxLoopAnim=1)
        self.animationIndexFat  = loadAnimationAsAsset(texture,"playerAnimFat",0.2,nbMaxLoopAnim=1)
        self.animationIndexTrans  = loadAnimationAsAsset(texture,"playerAnimTrans",0.1,nbMaxLoopAnim=4)

def playerLoadContent(texture,camera):
    playerWidth = 1.5
    playerHeight = 2.5

    path =  r".\noncolliders_sprite\player_yohann_lean_anim\yohann_player_1.png"
    loadImageAsAsset(texture,camera,"playerLean",(playerWidth,playerHeight),path)

    path =  r".\noncolliders_sprite\player_yohann_fat_anim\yohann_player_1.png"
    loadImageAsAsset(texture,camera,"playerFat",(playerWidth,playerHeight),path)

    pathFolderAnim = r".\noncolliders_sprite\player_yohann_fat_anim"
    loadImageListAsAsset(texture,camera,"playerAnimFat",(playerWidth,playerHeight),pathFolderAnim)

    pathFolderAnim = r".\noncolliders_sprite\player_yohann_lean_anim"
    loadImageListAsAsset(texture,camera,"playerAnimLean",(playerWidth,playerHeight),pathFolderAnim)

    pathFolderAnim = r".\noncolliders_sprite\player_yohann_trans_anim"
    loadImageListAsAsset(texture,camera,"playerAnimTrans",(playerWidth,playerHeight),pathFolderAnim)

def playerUpdate(player,keys,dt,colliderGOList,texture):
    """ function which handles the update of the player element
    colliderList is a list of game objects the player can collide with """

    elem = player.elem
    colElemList = gameObjectListGetElemList(colliderGOList)
    #creation of inputs for Dynamical update - List of colliders
    
    inputRelatedForce = vec(0,0)

    if rectElemCheckLanded(elem,colElemList):
        magnitude = 50
    else:
        magnitude = 7
    
    if keys[pygame.K_d]:
        inputRelatedForce.x = inputRelatedForce.x + magnitude*elem.m
    if keys[pygame.K_q]:
        inputRelatedForce.x = inputRelatedForce.x - magnitude*elem.m
    if keys[pygame.K_z] and rectElemCheckLanded(elem,colElemList):
        inputRelatedForce.y = inputRelatedForce.y + 10*elem.m/dt
        player.jumpSound.play()    
    if keys[pygame.K_s]:
        inputRelatedForce.y = inputRelatedForce.y - magnitude*elem.m
      
    collisionDescriptor = rectElemDynamicalUpdate(elem,dt,colElemList,inputRelatedForce)

    if player.elem.pos.y <-1:
        player.elem.pos.y = player.elem.pos.y + 15

    
    renderState = rectElemUpdateRender(elem,dt,texture)
    
    
    if player.phase == "fat" :
        
        if elem.velocity.magnitude() > 0.2 :
            rectElemBindAnim(elem,player.animationIndexFat)
        else:
            rectElemBindImage(elem,"playerFat")

    elif player.phase == "lean":
        if elem.velocity.magnitude() > 0.2 :
            rectElemBindAnim(elem,player.animationIndexLean)
        else:
            rectElemBindImage(elem,"playerLean")
    else:
            if renderState[0] and not renderState[1]:
                
                player.phase = "fat"
    
   
    
    

    if collisionDescriptor["collision"]:
        #if collision
        for i,direc in enumerate(collisionDescriptor["directions"]):
            #for each elemnt of colision
            if not direc and collisionDescriptor["senses"][i]:
                #if direction = Y and sens = positive
                hitGO = colliderGOList[collisionDescriptor["indices"][i]]
                if hitGO.label == "Block":
                    blockOnHit(hitGO)
    #checking for block hit from below

def playerRender(player,camera,screen,texture,showHitBox):
    flipX = False
    if player.elem.velocity.x < 0 :
        flipX = True
    rectElemRender(player.elem,screen,camera,texture,showHitBox,flip=(flipX,False))

def playerPowerUp(player):
    player.phase = "trans"
    rectElemBindAnim(player.elem,player.animationIndexTrans)

""" ============================= TERRAIN SECTION ================================="""

class Terrain():
    """ element of terrain which the player can collide with """
    def __init__(self,position):
        self.label = "Terrain"
        self.alive = True
        self.elem = RectElem(position,30,2,(0,255,0))
        rectElemBindImage(self.elem,"terrain")

def terrainLoadContent(texture,camera):
    path =  r".\colliders_sprites\terrain_collider.png"
    loadImageAsAsset(texture,camera,"terrain",(30,2),path)
    

""" ============================== SQUARE SECTION =================================="""

class Square():
     """ block which the player can collide with """
     def __init__(self,position):
        self.label = "Square"
        self.alive = True
        self.elem = RectElem(position,1,1,(0,255,0))
        rectElemBindImage(self.elem,"block")

""" ============================== BLOCK SECTION =================================="""

class Block():
     """ block which the player can collide with """
     def __init__(self,texture,position):
        self.label = "Block"
        self.alive = True
        self.elem = RectElem(position,0.75,0.75,(0,255,0))
        self.phase = "init"
        #phases for blocks : init, breaking, broken
        self.containedGO = None
        #game object contained in the block
        self.levelIndex = None
        rectElemBindImage(self.elem,"block")
        self.animationIndex  = loadAnimationAsAsset(texture,"blockAnim",0.1,nbMaxLoopAnim=1)
        

def blockLoadContent(texture,camera):
    """ Loads content in palette for block GO"""

    path =  r".\colliders_sprites\block_collider.png"
    loadImageAsAsset(texture,camera,"block",(0.75,0.75),path)
    #loading base image

    pathFolderAnim =  r".\anim_bloc"
    loadImageListAsAsset(texture,camera,"blockAnim",(0.75,0.75),pathFolderAnim)
    

def blockUpdate(block,texture,dt,):
    if block.phase == "init":
        rectElemUpdateRender(block.elem,dt,texture)
    if block.phase == "breaking":
        renderState = rectElemUpdateRender(block.elem,dt,texture)
        
        if not renderState[1]:
            block.phase = "broken"
            killGO(block)
            blockObject = block.containedGO
            if blockObject != None:
                resurectGO(blockObject)
                GOSetPosition(blockObject, block.elem.pos)


def blockSetLevelIndex(block, index):
    block.levelIndex = index

def blockOnHit(block):
    if block.phase == "init":
        block.phase = "breaking"
        rectElemBindAnim(block.elem,block.animationIndex)

def blockAddContainedGO(block,GO):
    """ add a gameObject to the the block which is activated upon block breaking GO must be in level"""
    killGO(GO)
    block.containedGO = GO


""" BIERE SECTION """

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
        



""" GOLDEN BEER SECTION"""

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
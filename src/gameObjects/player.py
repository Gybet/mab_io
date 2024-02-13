from gameObjects.GameObject import  gameObjectListGetElemList

from elements.IGRectElem import RectElem
from elements.commonRect import rectElemBindImage
from elements.commonRect import rectElemBindAnim
from elements.IGRectElem import rectElemEnableDynamics
from elements.IGRectElem import rectElemCheckLanded
from elements.IGRectElem import rectElemDynamicalUpdate

from MAB_IO_Camera import IGRectElemRender
from MAB_IO_Camera import loadImageAsAsset
from MAB_IO_Camera import loadAnimationAsAsset
from MAB_IO_Camera import loadImageListAsAsset
from MAB_IO_Camera import rectElemUpdateRender

import pygame
vec = pygame.Vector2

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
                    playerHitBlock(hitGO)
    #checking for block hit from below

def playerRender(player,camera,screen,texture,showHitBox):
    flipX = False
    if player.elem.velocity.x < 0 :
        flipX = True
    IGRectElemRender(player.elem,screen,camera,texture,showHitBox,flip=(flipX,False))



def playerHitBlock(block):
    if block.phase == "init":
        block.phase = "breaking"
        rectElemBindAnim(block.elem,block.animationIndex)
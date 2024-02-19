#Main Loop for MABIO
#version 1.1 


from gameObjects import *
from level_API import *

import os

from camera import cameraUpdate

Rect = pygame.Rect
vec = pygame.Vector2
mx = pygame.mixer


from gameObjects.block import *
from gameObjects.beer import *
from gameObjects.goldenBeer import *
from gameObjects.terrain import *
from gameObjects.player import *
from gameObjects.background import *
from gameObjects.enemy import *


    
""" ===========LEVEL SECTION =============="""
def levelLoad(level,texture,powerUpSound):
    
    terrain1 = Terrain(vec(0,0))
    terrain2 = Terrain(vec(30,0))
    levelAddGameObject(level,"terrain",terrain1)
    levelAddGameObject(level,"terrain",terrain2)
    #adding a collider to level's terrain list

    
    def pyramidCollidersPositions():
        positions = []

        for j in range(5):
            for i in range(2*j+1):
                positions.append(vec(15+(i-j)*0.75 , 5-j*0.75))

        return positions
    
    #pyramidPositionList = pyramidCollidersPositions()
    #for pos in pyramidPositionList:
        #square  = Square(pos)
        #levelAddGameObject(level,"square",square)


    def addBlock2Level(texture,level,x,y):
        block = Block(texture,vec(x,y))
        #block object generation
        ind = levelAddGameObject(level,"block",block)
        #block object added in level
        blockSetLevelIndex(block,ind)
        #setting blocks' levelIndex
        return block



    addBlock2Level(texture,level,6,5.5) 
    addBlock2Level(texture,level,6.75,5.5) 
    middleBlock = addBlock2Level(texture,level,7.5,5.5)
    addBlock2Level(texture,level,8.25,5.5) 
    addBlock2Level(texture,level,9,5.5)

    beer = Beer(vec(6,3))
    levelAddGameObject(level,"beer",beer)

    goldenBeer = GoldenBeer(vec(6,8),powerUpSound)
    levelAddGameObject(level,"goldenBeer",goldenBeer)
    blockAddContainedGO(middleBlock,goldenBeer)

    background = Background(vec(0,0))
    levelAddGameObject(level,"background",background)

    enemy = Enemy(vec(10,6))
    levelAddGameObject(level,"enemy",enemy)


""" ========== TEXTURE LOAD SECTION ============"""

def textureLoad(texture,camera):

    playerLoadContent(texture,camera)
    terrainLoadContent(texture,camera)
    blockLoadContent(texture,camera)
    beerLoadContent(texture,camera)
    goldenBeerLoadContent(texture,camera)
    backgroundLoadContent(texture,camera)


mx.init()
mx.music.load(r".\content\sound\music.mp3")
jumpSound = mx.Sound(r".\content\sound\jump.mp3")

powerUpSound = mx.Sound(r".\content\sound\powerUp.mp3")
pygame.mixer.music.play()

camera,texture,screen = GORenderInit()
textureLoad(texture,camera)

# pygame setup


clock = pygame.time.Clock()
running = True
dt = 1/60  

playerInitPos = vec(0,3)
player = RectPlayer(playerInitPos,texture,jumpSound)
#player init


level = levelInitiate()
levelLoad(level,texture,powerUpSound)
#level init, colliders instanciation and image loading in palette


showHitBox = False

keyLock = 0



""" Boucle de gameplay"""

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
    keys = pygame.key.get_pressed()
    keyLock = keyLock+ dt
    if keys[pygame.K_o]:
        #special key for debug and test
        showHitBox = not showHitBox
        if keyLock > 0.3:            
            keyLock = 0

    """ GO update"""
    blockList = levelGetGOsByKey(level,"block")
    terrainList = levelGetGOsByKey(level,"terrain")
    beerList = levelGetGOsByKey(level,"beer")
    gBeerList = levelGetGOsByKey(level,"goldenBeer")
    background = levelGetGOsByKey(level,"background")[0]
    enemyList = levelGetGOsByKey(level,"enemy")

    colliderGOList = terrainList + blockList  
    playerUpdate(player,keys,dt,colliderGOList,texture)
    #Player update

    
    for block in blockList:
        blockUpdate(block,texture,dt)
    #blocks update
        
    for beer in beerList:
        beerUpdate(beer,player)

    for gBeer in gBeerList:
        goldenBeerUpdate(gBeer,player,dt,colliderGOList)

    for enemy in enemyList:
        enemyUpdate(enemy,dt,colliderGOList)


    """ render """
    cameraUpdate(camera,player)
    #camera Update

    backgroundRender(background,screen,camera,texture)
    #background render

    interractiveGOs = blockList + terrainList + beerList + gBeerList + enemyList
    gameObjectListRender(interractiveGOs,screen,camera,texture,showHitBox)
    # rendering all elements in level
    
    playerRender(player,camera,screen,texture,showHitBox)
    #rendering player 

    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000


pygame.quit()





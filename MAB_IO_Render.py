import pygame
from os import listdir
from MAB_IO_Utilities import *
import math
Rect = pygame.Rect
vec = pygame.Vector2


""" ==========ANIMATION SECTION ============="""
class Animation():
    """ class used to define animations to render on screen
    used to display a succession of image on a rectangle surface"""
    
    def __init__(self, deltaT, key = "", nbMaxLoop = 0,alive = True):
       
        self.deltaT = deltaT
        #delta is the duration between each frame
        self.key = key
        self.clock = 0
        self.nbMaxLoop = nbMaxLoop
        #maximum nb of iteration before the animation deactivates, 0 means the animation goes on forever
        self.iter = 1
        #nb of time the animation has played
        self.duration = 0
        #duration of one iteration

        self.alive = alive
        #determine if the animation is in a state of being played or not


def animationSetDuration(animation,NbOfImage):
    """ This function must be called before trying to render an animation
    it sets the duration of the animation based on the number of image"""

    animation.duration = NbOfImage * animation.deltaT


def animationUpdate(animation,dt):

    animation.clock = animation.clock + dt
    print(animation.key)
    if animation.clock > animation.duration :
        #if iteration comes at an end
        if animation.iter == animation.nbMaxLoop:
            
            #if iteration was last iteration
            animation.clock = 0
            animation.alive = False
        else:
            
            animation.iter = animation.iter + 1
            animation.clock = animation.clock%animation.duration

    return (animation.alive,animation.iter)

    
    
    

""" ========== PARTICLE SECTION ============="""

class ParticleEffect():
    """ class used to render particles effect
     display images wich are moving without regard for physics"""

    def __init__(self,imageListKey,funcMat,nbPartMat,loop = False, nbLoop = 1,duration = 1):
        self.imgsKey = imageListKey
        # key of the multi image element witch makes the particle effect
        self.motionMat = funcMat
        #motion functions are of kind t : -> (vec2)
        self.nbPartMat = nbPartMat
        # list which represents the number of particle element drawn for each img of the multi image element
        self.loop = loop
        self.nbLoop = nbLoop
        self.duration = duration
        #duration in sec of each loop
        self.clock = 0
        #internal clock of the particule effect



def partEffectUpdate(partEffect,dt):
    partEffect.clock = (partEffect.clock + dt)%partEffect.duration



""" ========= Render Engine ================="""






"""  drawing function"""

def drawRectTransparentBackground(screen,rect,lineWidth = 1 , color = (255,0,0)):

    rec = Rect(rect[0],rect[1],rect[2],rect[3])
    pygame.draw.rect(screen,pygame.Color(color),rec,lineWidth)

def drawAnim(animIndex,texture,screen,rect,flip= (False,False)):
    """ draws an animation at the corresponding rectangle on screen"""
    anim = texture.animations[animIndex]
    index = int(anim.clock//anim.deltaT)
    imgList = texture.multiPalette[anim.key]
    index = index%len(imgList)
    img = imgList[index]
    imgFlipped = pygame.transform.flip(img,flip[0],flip[1])
    imgFlipped.set_colorkey(img.get_colorkey())
    screen.blit(imgFlipped , rect)
    
    
def drawPartEffect(texture,index,screen,rect):
    partEffect = texture.partEffects[index]
    imgList = texture.multiPalette[partEffect.imgsKey]

    for i,img in enumerate(imgList):
        for j in range(partEffect.nbPartForImgList[i]):
            
            deltaFunc = partEffect.motionMat[i][j]
            deltaPos = deltaFunc(partEffect.clock)
            deltaRec = rect.move(deltaPos.x,deltaPos.y)

            screen.blit(img,deltaRec)
                
def drawImage(texture,screen,imgRect,imgKey, flip = (False,False) ):
    image = texture.palette[imgKey]
    imgFlipped = pygame.transform.flip(image,flip[0],flip[1])
    imgFlipped.set_colorkey(image.get_colorkey())
    screen.blit(imgFlipped,imgRect)
    #drawing image 

def drawer(screen,texture,solidDraws = [],imageDraws = [],animationDraws = [],particulesDraws = []):
    """ Function that manages the draw of all games elements on the screen
    DRAWS are list in [(colorCode/key/index , rectangle), ... ,] format """
    #drawing background

    
    for solidDrawCall in solidDraws :
        rect = solidDrawCall[1]
        pygame.draw.rect(screen,pygame.Color(solidDrawCall[0]),rect)
        #drawing solid color draw calls


    for imgDrawCall in imageDraws :
        imgRect = imgDrawCall[1]
        image = texture.palette[imgDrawCall[0]]
        screen.blit(image,imgRect)
        #drawing image draw calls

    for animDrawCall in animationDraws:
        rect = animDrawCall[1]
        drawAnim(animDrawCall[0],texture,screen,rect)
        #animation draw calls

    for partDrawCall in particulesDraws:
        rect = partDrawCall[1]
        drawPartEffect(texture,partDrawCall[0],screen,rect)
        #particle draw calls
         
    

#def FPSdrawer(screen,dt):
    #FPS = str(int(1/dt))
    #debug = font.render(FPS,True, (0,0,0))
    #screen.blit(debug,(0,0))

import pygame
from render import *
from texture_API import *
vec = pygame.Vector2

class Camera():
    """ Class used to store render configuration and updadte the area of game rendered on screen """
    
    def __init__(self,model2Screen,viewWidth,viewHeight):
        """ ratio corresponds to model to screen ratio """
        self.pos = vec(0,0)
        #camera position is defined in game model coordinates
        #the position corresponds to the lower left corner of the visible screen

        self.yInvtNegCamUpperLeft = vec(0,0)
        #it represents the position of upper left corner of camera, negative

        self.viewWidth= viewWidth
        self.viewHeight = viewHeight
        #correspond to the the size of the area shown on screen (in game model dimmension)

        self.model2ScreenRatio = model2Screen
        #correspond to the ratio between game model and screen dimmension

        self.screenWidth = int(model2Screen * viewWidth)
        self.screenHeight = int(model2Screen * viewHeight)

def cameraConvertSizeGM(camera,size):
    """ Converts size in (width,length) format from game model space to screen space"""
    width = size[0]
    height = size[1]
    return (width * camera.model2ScreenRatio , height * camera.model2ScreenRatio)

def cameraConvertRect(camera,rect):
    """ Takes a rect in (x,y,w,h) format in game model coordinates and returns its equivalent on screen"""
    
    yInvtRectUpperLeft = vec(rect[0] , -rect[1] - rect[3])
    posInScreenDir = v2Add(yInvtRectUpperLeft , camera.yInvtNegCamUpperLeft)
    posOnScreen = v2Scal(camera.model2ScreenRatio , posInScreenDir)
    widthOnScreen = camera.model2ScreenRatio * rect[2]
    heightOnScreen = camera.model2ScreenRatio * rect[3]
    
    return pygame.Rect(posOnScreen.x, posOnScreen.y,widthOnScreen,heightOnScreen)

def cameraUpdate(camera,player):
    playerCenterX = player.elem.pos.x + player.elem.width/2
    camera.pos.x = playerCenterX - camera.viewWidth/2
    camera.yInvtNegCamUpperLeft = vec(-camera.pos.x , camera.pos.y + camera.viewHeight)


"""================== IMAGE LOADING SECTION =============="""
def imageFromFile(path,dimensions,colorKey):
    """ loads an image uses pygame.convert() and returns the result"""
    img = pygame.image.load(path)
    img.convert()
    img = pygame.transform.scale(img,dimensions)
    img.set_colorkey(colorKey)
    return img

def loadImageAsAsset(texture,camera,key,size,path,mode = "gameModel",colorKey = (255,0,255)):
    """ Takes a key, the path of an image and the size of render in game model and loads the corespond asset in texture object"""
    
    if mode == "gameModel":
        imgSize = cameraConvertSizeGM(camera , (size[0] , size[1]))
    else :
        imgSize = (size[0]*camera.screenWidth , size[1]*camera.screenHeight)
    
    image = imageFromFile(path,imgSize,colorKey)
    textureAPILoadImage(texture,key,image)

""" =================== IMAGELIST LOADING SECTION ================"""
def imageListFromFolder(folderPath,dimensions,colorKey):
    """ loads and convert all files in the given folder to images, all images at set at the same dimension
    returns them in a list"""
    images = []
    files = listdir(folderPath)
    for file in files:
        img = imageFromFile(folderPath + "\\" + file ,dimensions,colorKey)
        images.append(img)
    return images

def loadImageListAsAsset(texture,camera,key,size,folderPath,mode="gameModel",colorKey = (255,0,255)):
    """ Loads all files in the folder as images and makes an asset of Texture out of them"""
    
    if mode == "gameModel":
        imgSize = cameraConvertSizeGM(camera , (size[0] , size[1]))
    else :
        imgSize = (size[0]*camera.screenWidth , size[1]*camera.screenHeight)
    imgList = imageListFromFolder(folderPath,imgSize,colorKey )
    textureAPILoadImageList(texture,key,imgList)


def loadAnimationAsAsset(texture,key,deltaT,nbMaxLoopAnim = 0):
    """generates an animation object, binds the given key to it and adds it to texture
    returns the index of the animation in texture.animations list"""
    
    anim = Animation(deltaT,key,nbMaxLoop =nbMaxLoopAnim)
    animationSetDuration(anim,len(textureAPIGetMultiImage(texture,key)))
    index = textureAPILoadAnimation(texture,anim)

    return index

def loadParticleEffectAsAsset(texture,key,funcMat,nbPartMat):
    """ generates a particleEffect object, binds an key of multiPalette and adds it to texture.partEffetcs
    returns the index of the particle effect in the texture.partEffects list
    funcList and nbImageList must be at least as long as the number of image corresponding to key in multiPalette"""
  
    partEffect = ParticleEffect(key,funcMat,nbPartMat)
    index = textureAPILoadParticleEffect(texture,partEffect)

    return index

def IGRectElemRender(elem,screen,camera,texture,showHitBox = False,flip = (False,False)):
    """ Call to the rendr module to draw the element on screen"""
    rectModel = (elem.pos.x, elem.pos.y, elem.width, elem.height)
    rectConverted = cameraConvertRect(camera,rectModel)
    
    if elem.hasImage:
        drawImage(texture,screen,rectConverted,elem.imageKey,flip)
    elif elem.hasAnim:
        drawAnim(elem.animIndex,texture,screen,rectConverted,flip)
    else:
        drawRectFilled(screen,rectConverted)
    if showHitBox:        
        drawRectTransparentBackground(screen,rectConverted,1)
          

def fixedRectElemRender(elem,screen,camera,texture,flip = (False,False)):

    if elem.hasImage:
         

         widthPX = elem.rect[2]*camera.screenWidth
         heightPX = elem.rect[3]*camera.screenHeight

         xPX = elem.rect[0]*camera.screenWidth
         yPX = (1-elem.rect[1]-elem.rect[3])*camera.screenHeight

         rectConverted = pygame.Rect(xPX,yPX,widthPX,heightPX)

         
         drawImage(texture,screen,rectConverted,elem.imageKey,flip)



def rectElemUpdateRender(elem,dt,texture):
    
    if elem.hasAnim:
        anim = textureAPIGetAnimation(texture,elem.animIndex)
        animationState = animationUpdate(anim,dt)
        renderState = (True, animationState[0],animationState[1])
        return renderState
    renderState = (False,True,0)
    #first element is type of render
    #second element is Alive for an animation, just True for an image
    #third element is nb of iter for an animation, 0 for an image
    return renderState
    

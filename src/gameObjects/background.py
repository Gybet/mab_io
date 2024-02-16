from elements.fixedRectElem import FixedRectElem
from elements.commonRect import rectElemBindImage
from camera import loadImageAsAsset
from camera import fixedRectElemRender

class Background:
    def __init__(self,position):
        self.label = "Background"
        self.alive = True
        self.elem = FixedRectElem(0,0,1,1)
        rectElemBindImage(self.elem,"background")

def backgroundRender(background,screen,camera,texture):
    fixedRectElemRender(background.elem,screen,camera,texture)
    

def backgroundLoadContent(texture,camera):
    backgroundPath  =  r".\content\images\sprites\background_sprite.png"
    loadImageAsAsset(texture,camera,"background",(1,1),backgroundPath, mode="relative")
    print("hello")



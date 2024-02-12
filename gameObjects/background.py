
from gameObjects.camera.MAB_IO_Camera import loadImageAsAsset
from gameObjects.elements.fixedRectElem import FixedRectElem
from gameObjects.elements.commonRect import rectElemBindImage


from gameObjects.camera.MAB_IO_Camera import loadImageAsAsset
from gameObjects.camera.MAB_IO_Camera import fixedRectElemRender

class Background:
    def __init__(self,position):
        self.label = "Background"
        self.alive = True
        self.elem = FixedRectElem(0,0,1,1)
        rectElemBindImage(self.elem,"background")

def backgroundRender(background,screen,camera,texture):
    fixedRectElemRender(background.elem,screen,camera,texture)
    

def backgroundLoadContent(texture,camera):
    backgroundPath  =  r".\background.png"
    loadImageAsAsset(texture,camera,"background",(40,20),backgroundPath)
    print("hello")



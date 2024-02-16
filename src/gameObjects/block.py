from gameObjects.GameObject import killGO
from gameObjects.GameObject import resurectGO
from gameObjects.GameObject import GOSetPosition
from elements.IGRectElem import RectElem
from elements.commonRect import rectElemBindImage
from camera import loadImageAsAsset
from camera import loadAnimationAsAsset
from camera import loadImageListAsAsset
from camera import rectElemUpdateRender

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

    path =  r".\content\images\sprites\block_sprite.png"
    loadImageAsAsset(texture,camera,"block",(0.75,0.75),path)
    #loading base image

    pathFolderAnim =  r".\content\images\animations\block_breaking_animation"
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
    

def blockAddContainedGO(block,GO):
    """ add a gameObject to the the block which is activated upon block breaking GO must be in level"""
    killGO(GO)
    block.containedGO = GO
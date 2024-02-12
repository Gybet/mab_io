from gameObjects.elements.IGRectElem import RectElem
from gameObjects.elements.IGRectElem import rectElemBindImage
from gameObjects.camera.MAB_IO_Camera import loadImageAsAsset


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
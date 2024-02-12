from gameObjects.elements.IGRectElem import RectElem
from gameObjects.elements.IGRectElem import rectElemBindImage


class Square():
     """ block which the player can collide with """
     def __init__(self,position):
        self.label = "Square"
        self.alive = True
        self.elem = RectElem(position,1,1,(0,255,0))
        rectElemBindImage(self.elem,"block")
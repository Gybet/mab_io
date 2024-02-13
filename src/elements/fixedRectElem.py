

class FixedRectElem():
    """ this class represent a rectangular element outside of the game model with a fixed position on screen
    it can be used of UI or background render"""

    def __init__(self, SRX,SRY, SRWidth, SRHeight,color = (255,0,0)):
        self.rect = (SRX,SRY,SRWidth,SRHeight)
        self.hasImage = False
        self.imageKey = None
        self.hasAnim = False
        self.animIndex = None





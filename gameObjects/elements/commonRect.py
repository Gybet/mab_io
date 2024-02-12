
def rectElemBindAnim(elem,index):
     elem.hasImage = False
     elem.imageKey = None
     #unbinding image

     elem.hasAnim = True
     elem.animIndex = index
     #binding anim

def rectElemBindImage(elem,key):
     elem.hasImage = True
     elem.imageKey = key
     elem.hasAnim = False
     elem.animIndex = None
""" ======================TEXTURE DEINITION ================================="""
class Texture():
    """ class which contains all loaded images transformed to the display size"""

    def __init__(self):

        self.palette = {}
        self.multiPalette = {}
        self.animations = []
        self.partEffects = []


""" ======================TEXTURE API - Loading functions ================================="""

def textureAPILoadImage(texture,key,image):
    """ Takes an image and a key and load it in the texture object"""
    texture.palette[key] = image

def textureAPILoadImageList(texture,key,imageList):
    """ Takes a list of images and a key and loads it in the texture Object"""
    texture.multiPalette[key] = imageList

def textureAPILoadAnimation(texture,animation):
    """ Takes an Animation and loads it in the texture Object returns the index in the texture object"""
    texture.animations.append(animation)
    return len(texture.animations)-1

def textureAPILoadParticleEffect(texture,partEffect):
    """ Takes an ParticleEffect and loads it in the texture Object returns the index in the texture object"""
    texture.partEffects.append(partEffect)
    return len(texture.partEffects)-1

def textureAPIGetMultiImage(texture,key):
    return texture.multiPalette[key]

def textureAPIGetAnimation(texture,index):
    return texture.animations[index]





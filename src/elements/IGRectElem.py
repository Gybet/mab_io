#Element Module
#Version 1.1

from rectPhysics import dynamics
from rectPhysics import integration
from rectPhysics import collisionHandler
from rectPhysics import collisionState2AABB
from rectPhysics import contactState2AABB
from rectPhysics import collisionState2AABB


import pygame
vec = pygame.Vector2
def v2Add(u,v):
    return vec(u.x + v.x , u.y + v.y)

class RectElem():
    """ This class corresponds to a rectangular element
    The most basic ability of a rect elem is being rendered with solid color rectangle at a specific position in game model space
    -RENDER- 
    => an image can be attributed to a rectElem so it can be used as render
    => an animation can be attributed to the rectElem so it can be used as render

    -Physics-
    => Dynamics can be activated so the rect Elem moves according to forces and handles collisions
    => isCollider option can be activated so dynamic rect elems can collide with the concerned rectElem
    
    all elem are supposed to respect the following interface : 

    .pos -> vec2 : position of the elem in the game space
    
    """

    def __init__(self,position,width,height,color):
            
            """ initializing physical parameter"""
            self.pos = position
            #pos is a vector2 indicating the position of the bottom left corner of the rectangle
            self.width = width
            self.height = height
            # (int or float) width and height of the player in game model space (not screen space)
            self.boundaries = (position.x , position.y , position.x + width, position.y + height)
            # boundaries represent each point of the rectangle
            """ physics parameters"""
            self.dynamicsEnabled =False
            #define if the dynamic behavior has been activated for this element

            self.isCollider = False
            #defines if dynamical colliders can collide with this one
            """ render parameter"""        
            self.color = color
            #(len3 tuple or list with value from 0 to 255) collider color in RGB when no image is bound
            
            self.hasImage = False
            #defines if an image is bound to the collider
            self.imageKey = None
            #key referencing the image in imgpalette used for rendering (none when no image is bound)
            
            self.hasAnim = False
            #defines if an animation is bound to the collider
            self.animIndex = None

            """ meta parameter"""
            self.alive = True
            #defines if the collider is considered for physics and rendering

""" DYNAMICS FUNCTIONS """

def rectElemEnableDynamics(elem,mass,velocity = vec(0,0), gravity = True , airFriction = True, solidFriction = True):
     """ This function take a rectElem for which dynmacis have not yet been activated and activates them"""
     elem.m = mass
     #(int or float)  mass used for force calculations
     elem.velocity = velocity
     #initial velocity
     elem.subject2gravity = gravity
     elem.subject2AirFriction =airFriction
     elem.subject2SolidFriction = solidFriction
     #booleans indicating which forces th player is subject to

def rectElemDynamicalUpdate(elem,dt,elemColliderList,inputRelatedForce):
     """updates dynamical parameters (position velocity acceleration)"""
     predictedPos, predictedVelocity, collisionDescriptor = rectElemDynamicsPrediction(elem,elemColliderList,inputRelatedForce,dt)
     rectElemSetDynamics(elem,predictedPos,predictedVelocity)
     #undating elements dynamical value
     return collisionDescriptor


def rectElemDynamicsPrediction(elem,collidersElemList,additionalForce,dt):
    bd = elem.boundaries
    velocity = elem.velocity
    pos = elem.pos
    
    collidersBd = [elem.boundaries for elem in collidersElemList]
    acceleration = dynamics(elem,collidersBd,additionalForce)
    
    deltaPos, deltaVelocity = integration(acceleration,velocity,dt)
    #computing acceleration, deltaVelocity and deltaPos


    finalDeltaPos,finalVelocityMask,collisionDescriptor = collisionHandler(bd,deltaPos,collidersBd)
    #call to collisionHandler (in general physics model) returns the indices of colliders collided
    
    finalVeloX = (velocity.x + deltaVelocity.x)*finalVelocityMask[0]
    finalVeloY = (velocity.y + deltaVelocity.y)*finalVelocityMask[1]
    
    predictedVelocity = vec(finalVeloX,finalVeloY)
    predictedPos = v2Add(pos,finalDeltaPos)
    
    return predictedPos,predictedVelocity,collisionDescriptor

def rectElemSetPosition(elem, position):
    elem.pos = position
    elem.boundaries  = (position.x , position.y , position.x + elem.width, position.y + elem.height)

def rectElemSetDynamics(elem,position,velocity):
    rectElemSetPosition(elem,position)
    elem.velocity = velocity


def rectElemCheckLanded(elem1,envir):
    """ takes an element 1, and a list of elements and checks if element 1 is landed on another element"""
    landed = False
    bd1 = elem1.boundaries
    for elemEnvir in envir:
        elemEnvirBd = elemEnvir.boundaries

        collisionState = collisionState2AABB(bd1,elemEnvirBd)
        contactState = contactState2AABB(bd1,elemEnvirBd)

        contactBottom = (not collisionState[2] and contactState[2] and collisionState[0] and collisionState[1])

        landed = landed or contactBottom
        
    return landed

def checkProximity(elem1,elem2,directionRadius):
    """ check if elem2 is in the proximity of elem1 according to directionRadius
    direction radius = (x1,y1,x2,y2) where x1 is the distance from right of elem 1, y2 from the top etc..."""
    
    proximityCheck = collisionState2AABB(elem1.boundaries,elem2.boundaries,directionRadius)[4]

    return proximityCheck

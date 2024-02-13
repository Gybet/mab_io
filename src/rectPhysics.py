import pygame
from MAB_IO_Utilities import *
Rect = pygame.Rect
vec = pygame.Vector2


print("Physics engine loaded")

vecZero = vec(0,0)

""" ============ Physics Engine ========="""
""" ======================================"""

""" ====== I.1 forces  and dynamics functions ========="""

def gravityForce(mass):
    """ return a force corresponding to gravity"""
    g = 9.8
    power = mass * g
    return vec(0,-power)

def frictionForce(velocity):
    """ returns a vec2 corresponding to air friction force on elem"""
    # at low speed, friction force proportional to velocity is a valid approach
    f = 1.5
    return v2Scal(-f , velocity )


def uniformFieldForce(direction , power):
    """ direction --> vector 2 representing the direction of the force field
        power --> integer representing the power of the force field
        """
    return v2Scal(power , direction.normalize())

def solidFriction(elem1, colliderList,f, totalForce):
    """ compute solid friction force between a mobile element elem1 and colliders in colliderList
    elem1 must have a velocity and boundaries attribute
    colliders are in (x1,y1,x2,y2) format
    f is the solid drag coef, totalForce are all the other forces"""

    solidFric = vec(0,0)
    bd1 = elem1.boundaries
    for colRect in colliderList:
    
        collisionState = collisionState2AABB(bd1,colRect,offset = (0,0,0,0))
        contactState = contactState2AABB(bd1,colRect)

        

        contactLeft = (not collisionState[0] and contactState[0] and collisionState[2] and collisionState[3] )
        contactRight = (not collisionState[1] and contactState[1] and collisionState[2] and collisionState[3])
        contactBottom = (not collisionState[2] and contactState[2] and collisionState[0] and collisionState[1])
        contactTop = (not collisionState[3] and contactState[3] and collisionState[0] and collisionState[1])

        normalForceCoef = 0
        
        
        if contactLeft:
            if totalForce.x < 0:
                normalForceCoef = abs(totalForce.x)
                
            solidFric = v2Add(solidFric , vec(0,-f*normalForceCoef*elem1.velocity.y))
            
        elif contactRight:
            if totalForce.x > 0:
                normalForceCoef = abs(totalForce.x)

            solidFric = v2Add(solidFric , vec(0,-f*normalForceCoef*elem1.velocity.y))

        elif contactBottom:
            if totalForce.y <0:
                normalForceCoef = abs(totalForce.y)
                
            
            solidFric = v2Add(solidFric , vec(-f*normalForceCoef*elem1.velocity.x,0))
        elif contactTop:
            if totalForce.y >0:
                normalForceCoef = abs(totalForce.y)
            solidFric = v2Add(solidFric , vec(-f*normalForceCoef*elem1.velocity.x,0))
            
    return solidFric

def dynamics(elem,frictionElem,additionalForce = vecZero):
    """ returns a Vector2 corresponding to the acceleration of the element
    elem is a rectElem
    colliders is a list of element which induce solid friction on contact (only rect colliders are supported for now)
    additionnal Force is a vec2 corresponding for example to input induced Force"""

    totalForce = vec(0,0)
    totalForce = v2Add(totalForce,additionalForce)
    
    if elem.subject2gravity:
        totalForce = v2Add(totalForce , gravityForce(elem.m))
    
    if elem.subject2AirFriction:
        totalForce = v2Add(totalForce , frictionForce(elem.velocity))
        
    if elem.subject2SolidFriction:
        totalForce = v2Add(totalForce, solidFriction(elem,frictionElem,0.35,totalForce))
    
    fTot = v2Scal(1/elem.m , totalForce)

    return fTot

def integration(acceleration,velocity,dt):
    """ returns the delta of position for iteration t given the velocity and acceleration of iteration t-1"""
    deltaPos = v2Add( v2Scal(dt, velocity),
                      v2Scal(0.5*dt**2,acceleration))
    
    deltaVelocity = v2Scal(dt,acceleration)
    
    return deltaPos,deltaVelocity

""" ======== I.2 Collision handling functions ======== """
""" general physics functions"""

def collisionState2AABB(bd1,bd2,offset=(0,0,0,0)):
    """ Check collision between to rectangular object based on their boudnaries expressed in (x1,y1,x2,y2)
    offset is a dim 4 tuple where each value corrspond to the offset in one direction, positive offset = greater collision surface
    negative offset = lesser collision surface"""
    
    a = bd1[0] < bd2[2] + offset[2] #collision left 1 - right 2
    b = bd1[2] > bd2[0] - offset[0] #collision right 1 - left 2
    c = bd1[1] < bd2[3] + offset[3] #collision bottom 1 - top 2   
    d = bd1[3] > bd2[1] - offset[1] #collision top 1 - bottom 2
    #each of these boolean correspond to a a kind of boundary cross
    
    e = a and b and c and d
    #correspond to the collision check (True = Collision = every boundary cross is happening)
    return [a , b , c , d, e]

def contactState2AABB(bd1,bd2):
    contactThreshhold = 0.0001
    offset = (contactThreshhold,contactThreshhold,contactThreshhold,contactThreshhold)

    return  collisionState2AABB(bd1,bd2,offset)
    

def AABBsInCollision(bd1,bdList):
    """returns the indices of elements of bdList which collide with bd1 
    bd1 is a boundary given in (x1,y1,x2,y2) format
    bdList is a list of boundary to check the collision with"""

    collidedList = []
    for i,colElem in enumerate(bdList):
        collides = collisionState2AABB(bd1,colElem)[4]
        if collides:
            collidedList.append(i)
            
    return collidedList
            
    

def moveRate2Collision(bd1,deltaPos,bd2):
    """ returns the fraction of deltaPos the player can move to come in contact with the collider and boolean indicating on which axis the collision occurs
    takes 2 boundaries (bd1 and bd2) in (x1,y1,x2,y2) format such as bd1 is supposed to collide bd2
    takes velocity and deltaPos of elem1"""
    
    spdThreshold = 0.00001
    collideState = collisionState2AABB(bd1 ,bd2)
    collideLeft = collideState[0]
    collideRight = collideState[1]
    collideBottom = collideState[2]
    collideTop = collideState[3]

    minDistance = 0.00001
    #makes a minimal distance between the two object colliding to avoid penetration due to floats approx
    
    xCollisionPossible = False
    yCollisionPossible = False

    deltaX = 0
    deltaY = 0

    positiveSenseX = None
    positiveSenseY = None
    
    if abs(deltaPos.x) < spdThreshold and deltaPos.y <-spdThreshold:
        #vecteur vitesse direction : bas
        #collision face basse1 - haut2

        yCollisionPossible = True
        deltaY = bd2[3] - bd1[1] + minDistance
        positiveSenseY = False
        #deltaY <0
   
        

    elif deltaPos.x > spdThreshold  and deltaPos.y >spdThreshold:
        #vecteur vitesse direction : diag haut-droit
        #collision face haute1 - basse2 ou droite1- gauche 2

        if not collideRight:
            #potential collision on right
            xCollisionPossible = True
            deltaX = bd2[0] - bd1[2] - minDistance
            positiveSenseX = True
            #deltaX >0

        if not collideTop: 
            #potential collision on top
            yCollisionPossible = True
            deltaY = bd2[1]- bd1[3] - minDistance
            positiveSenseY = True
            #deltaY >0
            
        
    elif deltaPos.x > spdThreshold and abs(deltaPos.y) < spdThreshold:
        #velocity vector : right
        #collision on right1 - left2
        
        xCollisionPossible = True
        deltaX = bd2[0]  - bd1[2] - minDistance

        positiveSenseX = True
        #deltaX >0

    elif deltaPos.x > spdThreshold  and deltaPos.y < -spdThreshold:
        #vecteur vitesse direction : diag bas-droit
        #collision face basse1 - haute2 ou droite1- gauche 2
        
        if not collideRight:
            #potential collision on right
            xCollisionPossible = True
            deltaX = bd2[0] - bd1[2] - minDistance

            positiveSenseX =True
            #deltaX >0
            

        if not collideBottom:
            #potential collision on bottom
            yCollisionPossible = True
            deltaY = bd2[3] - bd1[1] + minDistance

            positiveSenseY =False
            #deltaY<0


    elif abs(deltaPos.x) <spdThreshold  and deltaPos.y >spdThreshold:
        #velocity vector up
        #collision on top 1 - bottom 2
        yCollisionPossible = True
        deltaY = bd2[3] - bd1[1] - minDistance

        positiveSenseY =True
        #deltaY >0

    elif deltaPos.x < -spdThreshold  and deltaPos.y < -spdThreshold:
        #vecteur vitesse direction : diag bas-gauche
        #collision face basse1 - haute2 ou gauche1- droite 2

        if not collideLeft:
            #potential collision on left
            xCollisionPossible = True
            deltaX = bd2[2] - bd1[0] + minDistance

            positiveSenseX = False
            #deltaX <0
            
        if not collideBottom:
            #potential collision on bottom
            yCollisionPossible = True
            deltaY = bd2[3] - bd1[1] + minDistance

            positiveSenseY = False
            #deltaY <0
            
    elif deltaPos.x < -spdThreshold and abs(deltaPos.y) <spdThreshold:
        #velocity vector left
        #collision face gauche1 - droite2
        xCollisionPossible = True
        deltaX = bd2[2] - bd1[0] + minDistance

        positiveSenseX =False
        #deltaX <0
        
    elif deltaPos.x < -spdThreshold  and deltaPos.y > spdThreshold:  
        #vecteur vitesse direction : diag haute-gauche
        #collision face haute1 - basse2 ou gauche1- droite 2
        
        if not collideLeft:
            #assured collision on left
            xCollisionPossible = True
            deltaX = bd2[2] - bd1[0] + minDistance

            positiveSenseX =False
            #deltaX <0

        elif not collideTop:
            #assured collision on top
            yCollisionPossible = True
            deltaY = bd2[1] - bd1[3] - minDistance

            positiveSenseY =True
            #deltaY > 0

    elif abs(deltaPos.x) <spdThreshold and deltaPos.y <-spdThreshold:
        #velocity vector down
        #collision face bottom1 - top2
        yCollisionPossible = True
        deltaY = bd2[1]- bd1[3] + minDistance

        positiveSenseY =False
        #deltaT < 0

    tx = 1
    ty = 1


    
    if xCollisionPossible:  
        tx = deltaX /deltaPos.x
        
    if yCollisionPossible:
        ty = deltaY/deltaPos.y

    if tx < ty:
        return tx,True,positiveSenseX
    
    else:    
        return ty,False,positiveSenseY

def moveRateNColliders(elem1,deltaPos,collidedList):
    """ returns the maximum fraction of velocity the element can move considering all the colliders """
    """ the fraction returned correspond to the point of contact with the first collider encountered"""
    """ returns the index of the collider in collidedList for which t is minimal"""
    """ elem1 must collide with all colliders in colidedList if deltaPos is applied"""
    
    tMin = 1
    directionX = False
    indMin = 0

    for i,colideElem in enumerate(collidedList):

        t,direc,positSense = moveRate2Collision(elem1,deltaPos,colideElem)     
                
        if t < tMin:
            tMin = t
            directionX = direc
            indMin = i
    
    return tMin,directionX,positSense,indMin


def collisionHandle1Axis(elem1,deltaPos,collidedList):
    """ returns the delta of position after collision is handled on one axis, and a velocity mask to apply on element 1"""
    
    t,directionX,positSense,ind = moveRateNColliders(elem1,deltaPos,collidedList)
    # returns the deltaPos ratio, the axis, and the index of the collider with which the collision must handled
    
    velocityMaskX=1
    velocityMaskY=1

    if directionX:
        #case where the earliest collision when moving by deltaPos is on X axis
        deltaX = deltaPos.x * t 
        velocityMaskX = 0
        return vec(deltaX, deltaPos.y),(velocityMaskX,velocityMaskY),True,positSense,ind
        

    else:
        #case where the earliest collision when moving by deltaPos is on Y axis
        deltaY = deltaPos.y * t 
        velocityMaskY = 0
        return vec(deltaPos.x, deltaY) , (velocityMaskX,velocityMaskY),False,positSense,ind


def collisionHandler(bd1,deltaPos,collidersBd):
    """ takes boundaries 1 , the expected delta of position of boundaries 1 and a list of boundaries to collides with
    and returns the actual delta of position wich boundaries 1 can move considering the collision with the list of boundaries """
    
    collisionDescriptor = {"collision":False,
                           #boolean indicating if collision happens
                           "indices":None,
                           #indices of colliders the object collides with
                           "directions":None,
                           #boolean True if collision happens on X axis, False if collision happens on the Y axis
                           "senses":None
                           #boolean indicating if collision happens towards positive space value, False for negative
                           }
    indsCollider = []
    directions = []
    senses = []
        
    virtualElem1 = (bd1[0] + deltaPos.x , bd1[1] + deltaPos.y, bd1[2] + deltaPos.x , bd1[3] + deltaPos.y)
    #construction of a virtual element wich corresponds to projected elem1 on next iteration
    
    indCollidedList1 = AABBsInCollision(virtualElem1,collidersBd)
    #list of indices of colliders in collision with projected elem1
    
    collidedList1 = [collidersBd[i] for i in indCollidedList1]
    #list of colliders in collisions with projected elem1
    
      
    if len(collidedList1) > 0 :
        #if a collision is detected
        collisionDescriptor["collision"] = True

        deltaPos1AxisHandled,velocityMask1,directionX,positSense,ind = collisionHandle1Axis(bd1,deltaPos,collidedList1)
        virtualElem2 = (bd1[0] + deltaPos1AxisHandled.x,
                        bd1[1] + deltaPos1AxisHandled.y,
                        bd1[2] + deltaPos1AxisHandled.x,
                        bd1[3] + deltaPos1AxisHandled.y)
        
        indsCollider.append(indCollidedList1[ind])
        directions.append(directionX)
        senses.append(positSense)
        #adding the index of collider ,direction and sense of collision in lists
        
        
      
        #construction of the virtual Elem after the first axis of cillision hs been handled

        indCollidedList2 = AABBsInCollision(virtualElem2,collidersBd)
        #list of colliders in collision with the virtual elem2

        collidedList2 = [collidersBd[i] for i in indCollidedList2]
        #list of colliders in collisions with projected elem2
    
        if len(collidedList2) > 0 :
           
            deltaPosFinal, velocityMask2,directionX,positSense,ind = collisionHandle1Axis(bd1,deltaPos1AxisHandled,collidedList2)
            
            velocityMaskFinal = (velocityMask1[0] * velocityMask2[0],
                                 velocityMask1[1] * velocityMask2[1])
            
            indsCollider.append(indCollidedList1[ind])
            directions.append(directionX)
            senses.append(positSense)
            #adding the index of collider ,direction and sense of collision in lists

        else:
            deltaPosFinal = deltaPos1AxisHandled
            velocityMaskFinal = velocityMask1
    else:
        deltaPosFinal = deltaPos
        velocityMaskFinal = (1,1)

    collisionDescriptor["indices"] = indsCollider
    collisionDescriptor["senses"] =senses
    collisionDescriptor["directions"]= directions

    return deltaPosFinal,velocityMaskFinal,collisionDescriptor
    

def virtualPlayerBoundaries(player , projection):
    """ return the boundaries of a virtual player based on an existing player and a position projection"""
    x1 = projection.x
    y1 = projection.y
    x2 = projection.x + player.width
    y2 = projection.y + player.Height

    return (x1,y1,x2,y2)



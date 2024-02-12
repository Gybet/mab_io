from MAB_IO_Element import * 
import pygame
vec = pygame.Vector2

testElem = RectElem(vec(0,0),1,1,15,(0,0,0))
#testElem.subject2AirFriction = False


for i in range(1000):
    nextPos,nextVel = rectElemDynamicsPrediction(testElem,[],vec(0,0),0.05)
    print(nextPos)
    rectElemSetDynamics(testElem,nextPos,nextVel)
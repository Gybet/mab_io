""" UTILITIES FUNCTIONS"""
import pygame
vec = pygame.Vector2

def v2Add(u,v):
    return vec(u.x + v.x , u.y + v.y)

def v2Scal(alpha,v):
    return vec(alpha*v.x , alpha*v.y)


def camViz(camera):
    x1 = "x1 : " + str(camera.pos.x)
    y1 = "y1 : " + str(camera.pos.y)
    x2 = "x2 : " + str(camera.pos.x + camera.viewWidth)
    y2 = "y2 : " + str(camera.pos.y + camera.viewHeight)
    
    return x1 + "\n" + y1 + "\n" + x2 + "\n" +y2 + "\n"






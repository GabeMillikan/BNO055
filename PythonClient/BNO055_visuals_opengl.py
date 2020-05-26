import pygame
from pygame.locals import *
from BNO055 import BNO055
bno = BNO055()

# Y+ up
from OpenGL.GL import *
from OpenGL.GLU import *


verticies = [
    (-0.75,  -0.1, -1.5),
    ( 0.75,  -0.1, -1.5),
    ( 0.75,  -0.1,  1.5),
    (-0.75,  -0.1,  1.5),
    
    (-0.75,   0.1, -1.5),
    ( 0.75,   0.1, -1.5),
    ( 0.75,   0.1,  1.5),
    (-0.75,   0.1,  1.5),
    
    (0, 0, 0),
    (0, 1, 0),
]

edges = [
    (0,1),
    (1,2),
    (2,3),
    (3,0),
    
    (4,5),
    (5,6),
    (6,7),
    (7,4),
    
    (0, 4),
    (1, 5),
    (2, 6),
    (3, 7),
    

    (-2, -1),
]


def Cube():
    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(verticies[vertex])
    glEnd()


pygame.init()
display = (800,600)
pygame.display.set_mode(display, DOUBLEBUF|OPENGL)

gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)

glTranslatef(0.0, 0.0, -5)
glRotatef(45, 0, 0, 0)

mousedown = False

try:
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                bno.die = True
                quit()
            
            if event.type == 5:
                mousedown = True
            if event.type == 6:
                mousedown = False
                
            if event.type == 4 and mousedown:
                print("dragging")
                x, y = pygame.mouse.get_rel()
                glRotatef(1, y, x, 0)
                

        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        Cube()
        pygame.display.flip()
        pygame.time.wait(10)
        
        # remap to new coordinate frame
        x,y,z = (bno.gravity/9.81).values
        verticies[-1] = (-y, -z, -x)
except BaseException as e:
    bno.die = True
    quit(e)
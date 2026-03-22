import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

pygame.init()

display = (800,600)

pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

glEnable(GL_DEPTH_TEST)

gluPerspective(60, display[0]/display[1], 0.1, 100)

glTranslatef(0,0,-10)

vertices = (
    (1,1,1),
    (1,1,-1),
    (1,-1,-1),
    (1,-1,1),
    (-1,1,1),
    (-1,1,-1),
    (-1,-1,-1),
    (-1,-1,1)
)

faces = (
    (0,1,2,3),
    (3,2,7,6),
    (6,7,4,5),
    (5,4,0,1),
    (1,5,6,2),
    (4,0,3,7)
)

clock = pygame.time.Clock()

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glRotatef(1,1,1,0)

    glBegin(GL_QUADS)

    for face in faces:
        glColor3f(0.8,0.2,0.2)
        for vertex in face:
            glVertex3fv(vertices[vertex])

    glEnd()

    pygame.display.flip()

    clock.tick(60)
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

"""
문제
1. display라는 변수를 생성하고, 원하는 화면 크기를 크기 2의 tuple로 할당해주세요.
2. faces라는 list를 생성하고, 아래와 같은 tuple로 구성하도록 작성해주세요.
    - (0, 1, 2, 3)
    - (3, 2, 7, 6)
    - (6, 7, 4, 5)
    - (5, 4, 0, 1)
    - (1, 5, 6, 2)
    - (4, 0, 3, 7)
    
3. vertices라는 list를 생성하고, for문을 사용해서 다음과 같은 8개의 정점 좌표를 할당해주세요.
    - (1, 1, 1)
    - (1, 1, -1)
    - (1, -1, -1)
    - (1, -1, 1)
    - (-1, 1, 1)
    - (-1, 1, -1)
    - (-1, -1, -1)
    - (-1, -1, 1)

4. vertices에 선언된 점은 8개입니다.
    faces에서 이 점들이 3번씩 사용되었는지 if문을 사용하여 확인해주세요.
"""


display = (800,600)

vertices = [
    (1,1,1),
    (1,1,-1),
    (1,-1,-1),
    (1,-1,1),
    (-1,1,1),
    (-1,1,-1),
    (-1,-1,-1),
    (-1,-1,1)
]

faces = [
    (0,1,2,3),
    (3,2,7,6),
    (6,7,4,5),
    (5,4,0,1),
    (1,5,6,2),
    (4,0,3,7)
]

pygame.init()

pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

glEnable(GL_DEPTH_TEST)

gluPerspective(60, display[0]/display[1], 0.1, 100)

glTranslatef(0,0,-10)


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
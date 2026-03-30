import pygame
import math

from OpenGL.GL import *
from OpenGL.GLU import *


class UI:
    def __init__(self, width, height, heart_path, bullet_path, crosshair_path):

        self.width = width
        self.height = height

        self.heart_tex = self.load_texture(heart_path)
        self.bullet_tex = self.load_texture(bullet_path)
        self.crosshair_tex = self.load_texture(crosshair_path)

        pygame.font.init()
        self.font = pygame.font.SysFont("Arial", 32)

    def load_texture(self, path):
        surface = pygame.image.load(path).convert_alpha()
        surface = pygame.transform.rotate(surface, 180)
        image = pygame.image.tostring(surface, "RGBA", True)

        width = surface.get_width()
        height = surface.get_height()

        tex_id = glGenTextures(1)

        glBindTexture(GL_TEXTURE_2D, tex_id)

        glTexImage2D(
            GL_TEXTURE_2D,
            0,
            GL_RGBA,
            width,
            height,
            0,
            GL_RGBA,
            GL_UNSIGNED_BYTE,
            image
        )

        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

        return tex_id

    def draw_texture(self, tex, x, y, w, h):
        glBindTexture(GL_TEXTURE_2D, tex)

        glBegin(GL_QUADS)

        glTexCoord2f(0,1)
        glVertex2f(x,y)

        glTexCoord2f(1,1)
        glVertex2f(x+w,y)

        glTexCoord2f(1,0)
        glVertex2f(x+w,y+h)

        glTexCoord2f(0,0)
        glVertex2f(x,y+h)

        glEnd()

    def draw_text(self, text, x, y, color=(255,255,255)):
        surface = self.font.render(text, True, color)
        data = pygame.image.tostring(surface, "RGBA", True)

        w = surface.get_width()
        h = surface.get_height()

        glRasterPos2f(x, y)

        glDrawPixels(
            w,
            h,
            GL_RGBA,
            GL_UNSIGNED_BYTE,
            data
        )

    def draw_circle(self, cx, cy, r, segments=64):
        glBegin(GL_LINE_LOOP)
        for i in range(segments):
            theta = 2.0 * math.pi * i / segments
            x = cx + r * math.cos(theta)
            y = cy + r * math.sin(theta)

            glVertex2f(x, y)

        glEnd()

    def draw_crosshair(self, player):
        cx = self.width / 2
        cy = self.height / 2 + player.walk_bob * 400

        glDisable(GL_TEXTURE_2D)

        glColor3f(0, 1, 0)
        glLineWidth(2)

        self.draw_circle(cx, cy, 2)
        self.draw_circle(cx, cy, 18)
        glColor3f(1,1,1)
    
    def draw(self, player, ammo, score):
        glPushAttrib(GL_ENABLE_BIT | GL_COLOR_BUFFER_BIT)

        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        glOrtho(0, self.width, 0, self.height, -1, 1)

        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()

        glDisable(GL_DEPTH_TEST)
        glDisable(GL_TEXTURE_2D)
        glColor3f(1,1,1)

        self.draw_text(f"Score: {score}", 20, self.height - 40, (255,165,0))

        glEnable(GL_TEXTURE_2D)

        size = 40
        margin = 20
        spacing = 10

        for i in range(int(player.health/10)):
            x = self.width - margin - size - i * (size + spacing)
            y = margin

            self.draw_texture(self.heart_tex, x, y, size, size)

        for i in range(int(ammo)):
            x = self.width - margin - size - i * (size + spacing)
            y = self.height - size - 20

            self.draw_texture(self.bullet_tex, x, y, size, size)

        self.draw_crosshair(player)
        
        glPopMatrix()

        glMatrixMode(GL_PROJECTION)
        glPopMatrix()

        glMatrixMode(GL_MODELVIEW)

        glPopAttrib()
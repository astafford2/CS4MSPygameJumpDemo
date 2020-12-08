# Sprite Sheet Animation Demo

import pygame, sys
from pygame.locals import *

# initialize pygame
pygame.init()


##########################################
class SpriteSheetImage(pygame.sprite.Sprite):
    def __init__(self, target):
        pygame.sprite.Sprite.__init__(self)  # extend the base Sprite class
        self.master_image = None
        self.frame = 0
        self.old_frame = -1
        self.frame_width = 1
        self.frame_height = 1
        self.first_frame = 0
        self.last_frame = 0
        self.columns = 1
        self.last_time = 0

    # X property
    def _getx(self):
        return self.rect.x

    def _setx(self, value):
        self.rect.x = value

    X = property(_getx, _setx)

    # Y property
    def _gety(self):
        return self.rect.y

    def _sety(self, value):
        self.rect.y = value

    Y = property(_gety, _sety)

    # position property
    def _getpos(self):
        return self.rect.topleft

    def _setpos(self, pos):
        self.rect.topleft = pos

    position = property(_getpos, _setpos)

    def load(self, filename, width, height, columns):
        self.master_image = pygame.image.load(filename).convert_alpha()
        self.frame_width = width
        self.frame_height = height
        self.rect = Rect(0, 0, width, height)
        self.columns = columns
        # try to auto-calculate total frames
        rect = self.master_image.get_rect()
        self.last_frame = (rect.width // width) * (rect.height // height) - 1

    def update(self, current_time, rate=30):
        # update animation frame number
        if current_time > self.last_time + rate:
            self.frame += 1
            if self.frame > self.last_frame:
                self.frame = self.first_frame
            self.last_time = current_time

        # build current frame only if it changed
        if self.frame != self.old_frame:
            frame_x = (self.frame % self.columns) * self.frame_width
            frame_y = (self.frame // self.columns) * self.frame_height
            rect = Rect(frame_x, frame_y, self.frame_width, self.frame_height)
            self.image = self.master_image.subsurface(rect)
            self.old_frame = self.frame


##########################################
black = (0, 0, 0)

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("PyGame Jumping Demo")

clock = pygame.time.Clock()
ticks = pygame.time.get_ticks()

# Player
player = SpriteSheetImage(screen)
player.load("retro-character-sprite-sheet.png", 43, 64, 4)
playerGroup = pygame.sprite.Group()
playerGroup.add(player)
player.position = (400, 400)
player.frame = 0
player.first_frame = 0
player.last_frame = 0

xs = 0
ys = 0

while True:
    screen.fill(black)

    playerGroup.update(ticks, 70)
    playerGroup.draw(screen)
    
    player.X += xs
    player.Y += ys
    
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        if (event.type == pygame.KEYDOWN):
            if (event.key == pygame.K_r):
                player.position = (400, 400)

            if (event.key == pygame.K_UP):
                ys = -10
                player.frame = 4
                player.first_frame = 4
                player.last_frame = 7
            if (event.key == pygame.K_DOWN):
                ys = 10
                player.frame = 0
                player.first_frame = 0
                player.last_frame = 3
            if (event.key == pygame.K_LEFT):
                xs = -10
                player.frame = 8
                player.first_frame = 8
                player.last_frame = 11
            if (event.key == pygame.K_RIGHT):
                xs = 10
                player.frame = 12
                player.first_frame = 12
                player.last_frame = 15

        if (event.type == pygame.KEYUP):
            if (event.key == pygame.K_UP):
                ys = 0
                player.frame = 4
                player.first_frame = 4
                player.last_frame = 4
            if (event.key == pygame.K_DOWN):
                ys = 0
                player.frame = 0
                player.first_frame = 0
                player.last_frame = 0
            if (event.key == pygame.K_LEFT):
                xs = 0
                player.frame = 8
                player.first_frame = 8
                player.last_frame = 8
            if (event.key == pygame.K_RIGHT):
                xs = 0
                player.frame = 12
                player.first_frame = 12
                player.last_frame = 12

    clock.tick(30)
    ticks = pygame.time.get_ticks()
    pygame.display.update()

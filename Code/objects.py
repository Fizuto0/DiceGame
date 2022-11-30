import pygame as pg
import pygame.image
from pygame.math import Vector2 as vector
from forHelp.helpers import *
from Code.forHelp import autoload as autol
from settings import COLORKEY






class Gun(pg.sprite.Sprite):
    def __init__(self, start_pos,operator):
        super().__init__()
        autol.all_sprites.add(self)

        self.scale =2

        self.org_sprite = pygame.image.load('../Jpgs/rewolwer.png')
        self.org_sprite = pg.transform.scale(self.org_sprite,\
                        (self.org_sprite.get_width()*self.scale, self.org_sprite.get_height()* self.scale))
        self.org_sprite.set_colorkey(COLORKEY)

        self.operator = operator

        self.image = pg.Surface((pg.display.get_window_size()[0]*1.5,pg.display.get_window_size()[1]*1.5))
        self.image.fill((255,255,255))
        self.image.set_colorkey((255,255,255))
        self.rect = self.image.get_rect(center = start_pos)

    def set_place_image(self):
        self.image = pg.Surface((pg.display.get_window_size()[0]*1.5,pg.display.get_window_size()[1]*1.5))
        self.image.fill((255,255,255))
        self.image.set_colorkey(COLORKEY)

    def rotate_handler(self):
        if 90<self.operator.arm_angle<270:
            self.blit_sprite = pg.transform.rotate(pg.transform.flip(self.org_sprite,0,1),self.operator.arm_angle)
            #TODO add muzzle positions
        else:
            self.blit_sprite = pg.transform.rotate(self.org_sprite,self.operator.arm_angle)

    def shoot(self,card):
        card.shooted(self.pos, self.operator.arm_angle, self, self.operator)

    def update(self):
        self.set_place_image()
        self.rect.center =self.operator.arm_pos
        self.rotate_handler()
        self.pos = (self.image.get_width() / 2 - self.blit_sprite.get_width() / 2, \
                    self.image.get_height() / 2 - self.blit_sprite.get_height() / 2)
        self.image.blit(self.blit_sprite,self.pos)


class Dice(pg.sprite.Sprite):
    def __init__(self, start_pos, direction, operator):
        super().__init__()
        autol.all_sprites.add(self)

        self.sprite_org = pg.image.load('../Jpgs/dice.png')
        self.sprite_org.set_colorkey(COLORKEY)
        self.sprite = self.sprite_org

        self.alpha = 130

        self.operator = operator

        self.image = pg.Surface((20,20))
        self.image.fill(COLORKEY)
        self.image.set_colorkey(COLORKEY)
        self.image.set_alpha(self.alpha)
        self.rect = self.image.get_rect(center = start_pos)


        #collision, should be good
        self.collide_rect = pg.Rect(self.rect.left + self.image.get_width()/4, self.rect.top+self.image.get_height()/4,\
                                    self.sprite_org.get_width(),self.sprite_org.get_height())


        #move variable
        self.force = 12
        self.mov_var = vector(self.force,0)
        self.mov_var = self.mov_var.rotate(-direction)
        self.gravity = 0.2
        self.angle = 0
        if 90 < direction < 270:
            self.direction = direction /16
        elif 90> direction:
            self.direction = (direction-90)/5
        else:
            self.direction = (direction - 360)/4

    def set_image(self):
        self.image = pg.Surface((20, 20))
        self.image.fill(COLORKEY)
        self.image.set_colorkey(COLORKEY)
        self.image.set_alpha(self.alpha)

    def collide_handler(self):
        for collider in autol.collision_sprites:
            if collider.rect.colliderect(self.collide_rect) and collider != self.operator:
                self.kill() #TODO for later, change into collide rect

    def rotate(self):
        self.set_image()
        self.sprite = pg.transform.rotate(self.sprite_org, self.angle)
        self.image.blit(self.sprite, (self.image.get_size()[0]/2 - self.sprite.get_size()[0]/2,\
                                      self.image.get_size()[1]/2 - self.sprite.get_size()[1]/2))
        self.angle +=self.direction

    def update(self):
        self.rotate()
        self.collide_rect = pg.Rect(self.rect.left + self.image.get_width()/4, self.rect.top+self.image.get_height()/4,\
                                    self.sprite_org.get_width(),self.sprite_org.get_height())
        self.collide_handler()

        self.rect.x += self.mov_var.x
        self.mov_var.y += self.gravity
        self.rect.y += self.mov_var.y


class Card_Blueprint(pg.sprite.Sprite):
    def __init__(self, start_pos):
        super().__init__()
        autol.all_sprites.add(self)
        self.sprite = pg.image.load('../Jpgs/card.png')
        self.sprite.set_colorkey(COLORKEY)

        self.image = self.sprite
        self.rect = self.image.get_rect(center = start_pos)

        self.mov_vec = vector(0,1)

    def shooted(self, start_pos, angle, gun, player):
        pass #TODO functionality

    def collide_handler(self):
        #collision with player
        if self.rect.colliderect(autol.player.rect):
            autol.player.card_inventory.append(self)
            self.kill()
        #TODO collision with world floor

    def update(self):
        self.collide_handler()
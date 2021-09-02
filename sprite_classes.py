import pygame
import random
from pygame.constants import K_SPACE, RLEACCEL
from constants import COLOR_BLACK, COLOR_WHITE

#main sprite class used by all other sprite classes
class Sprites(pygame.sprite.Sprite):
    def __init__(self, screen_width, screen_height, center):
        super(Sprites, self).__init__()
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.center = center
        self.speedx = 0
        self.speedy = 0

    def get_center(self):
        return self.center

    def get_center_x(self):
        return self.center[0]

    def get_center_y(self):
        return self.center[1]

    def move(self):
        self.rect.move_ip(self.speedx, self.speedy)

#player sprite class used for ship
class Player(Sprites):
    def __init__(self, screen_width, screen_height, player_center):
        Sprites.__init__(self, screen_width, screen_height, player_center)
        self.file_list = ["images/player.png", "images/player_boost.png"]
        self.surf1 = pygame.image.load(self.file_list[0]).convert()
        self.surf1.set_colorkey(COLOR_BLACK, RLEACCEL)
        self.mask = pygame.mask.from_surface(self.surf1)
        self.rect = self.surf1.get_rect(center = player_center)

    #vertical acceleration
    def vertical_loss(self):
        self.speedy += 0.2

    #boost if space is pressed otherwise 
    def boost(self, pressed_key):
        self.vertical_loss()
        if pressed_key[K_SPACE]:
            self.speedy -= 0.4
            self.surf1 = pygame.image.load(self.file_list[1]).convert()
            self.surf1.set_colorkey((0, 0, 0), RLEACCEL)
            return 1
        else:
            self.surf1 = pygame.image.load(self.file_list[0]).convert()
            self.surf1.set_colorkey((0, 0, 0), RLEACCEL)
            return 0
    #update sprite location and check for boost
    def update(self, pressed_key):
        self.move()
        self.center = [self.rect.centerx, self.rect.centery]
        return self.boost(pressed_key)

#main class for backgrounds
class Background(Sprites):
    def __init__(self, screen_width, screen_height, background_center, file_image, color_key):
        Sprites.__init__(self, screen_width, screen_height, background_center)
        self.file_image = file_image
        self.surf1 = pygame.image.load(file_image).convert()
        self.surf1.set_colorkey(color_key, RLEACCEL)
        self.mask = pygame.mask.from_surface(self.surf1)
        self.rect = self.surf1.get_rect(center = background_center)
        
#wall sprites
class Wall(Background):
    def __init__(self, screen_width, screen_height, center , file_image):
        Background.__init__(self, screen_width, screen_height, center, file_image, COLOR_WHITE)
        self.flag = 0 #only need to add new wall once per wall
        self.score_flag = 0 #only need to update score once per wall

    def get_flag(self):
        return self.flag

    def set_flag(self, flag):
        self.flag = flag

    def get_score_flag(self):
        return self.score_flag

    def set_score_flag(self, flag):
        self.score_flag = flag

    #update position
    def update(self):
        self.speedx = -1
        self.center = [self.rect.centerx, self.rect.centery]
        self.move()

#smoke sprites
class Smoke(Background):
    def __init__(self, screen_width, screen_height, center , file_image):
        Background.__init__(self, screen_width, screen_height, center, file_image, COLOR_WHITE)
    
    #update position
    def update(self):
        #move smoke slowly downward
        if random.randint(0,10) == 1:
            self.speedy = 1
        else:
            self.speedy = 0
        #move smoke left at the same time as the walls   
        self.speedx = -1
        self.center = [self.rect.centerx, self.rect.centery]
        self.move()

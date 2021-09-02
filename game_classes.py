import pygame
import random
import math
from pygame.constants import K_SPACE
import sprite_classes
from constants import *

class Game_Text():
    def __init__(self, win, width, height):
        self.width = width
        self.height = height
        self.text_list = []
        self.font = pygame.font.Font('freesansbold.ttf', 32) #font used for all text
        self.win = win
        self.score = 0
        self.high_score = 0
        self.game_over_width = (self.width/2) - 100
        self.game_over_height = (self.height/2) - 32
        self.score_padding = 125 
        self.high_score_padding = 200
        self.score_pad_num = 10
        self.high_score_pad_num = 10

    def get_score(self):
        return self.score

    def get_high_score(self):
        return self.high_score

    def set_score(self, score):
        self.score = score

    def set_high_score(self, high_score):
        self.high_score = high_score

    def padding(self):
        if self.score / self.score_pad_num == 1:
            self.score_padding += 10
            self.score_pad_num *= 10

        if self.high_score / self.high_score_pad_num == 1:
            self.high_score_padding += 10
            self.high_score_pad_num *= 10

    def update_score(self):
        self.padding()
        if self.score > self.high_score:
            self.high_score = self.score
        self.text_list[3] = self.font.render(str(self.score), False, COLOR_WHITE)
        self.text_list[4] = self.font.render(str(self.high_score), False, COLOR_WHITE)
        
    def create_text(self):
        text_score = self.font.render('Score:', False, COLOR_WHITE)
        text_game_over = self.font.render('Game Over', False, COLOR_WHITE)
        text_high_score = self.font.render('High Score:', False, COLOR_WHITE)
        score = self.font.render(str(self.score), False, COLOR_WHITE)
        high_score = self.font.render(str(self.high_score), False, COLOR_WHITE)
        self.text_list = [text_score, text_game_over, text_high_score, score, high_score]  

    def update_text(self, game_status):
        if game_status == 0:
            self.update_score()
            self.win.blit(self.text_list[0], (5, 10)) #text_score
            self.win.blit(self.text_list[2], (0, HEIGHT - 40))  #text_high_score
            self.win.blit(self.text_list[3], (self.score_padding, 10))  #score
            self.win.blit(self.text_list[4], (self.high_score_padding, HEIGHT - 40))  #high_score
        else:
            self.win.blit(self.text_list[0], (5, 10)) #text_score
            self.win.blit(self.text_list[3], (self.score_padding, 10))  #score
            self.win.blit(self.text_list[1], (self.game_over_width, self.game_over_height)) #text_game_over
            self.win.blit(self.text_list[2], (5, HEIGHT - 40)) #text_high_score
            self.win.blit(self.text_list[4], (self.high_score_padding, HEIGHT - 40))  #high_score

class Game():
    def __init__(self, clock_speed, rgb_tuple, win, width, height):
        self.width = width
        self.height = height
        self.win = win
        self.text = Game_Text(win, width, height)
        self.game_status = 0
        self.player_start = [width/4, height/2]
        self.player = sprite_classes.Player(WIDTH, HEIGHT, self.player_start)
        self.background = sprite_classes.Background(WIDTH, HEIGHT, [width/2, height/2], "images/background.png", COLOR_WHITE)
        self.walls = pygame.sprite.Group()
        self.top_walls = pygame.sprite.Group()
        self.bottom_walls = pygame.sprite.Group()
        self.smoke = pygame.sprite.Group()
        self.surfaces = pygame.sprite.Group()
        self.clock = pygame.time.Clock()
        self.clock_speed = clock_speed
        self.win_rgb = rgb_tuple
        self.number_players = 1
        self.max_point = 1100
        self.last_top = 0
        self.last_bottom = 800

    def get_status(self):
        return self.game_status

    #functions for cleaning up sprites
    def remove_walls(self):
        self.wall_list = []
        for wall in self.wall_top:
            wall.kill()
        for wall in self.wall_bottom:
            wall.kill()

    def remove_sprites(self):
        self.surfaces = pygame.sprite.Group()

    def create_walls(self):
        centerx = 48 + 96 * 8
        number_of_walls = 13
        for i in range(number_of_walls):
            self.add_wall(centerx)
            centerx += 96

    #functions for game progression
    def start(self):
        self.add_sprites()
        self.create_walls()
        self.read_high_score()
        self.text.create_text()

    def restart(self):
        self.remove_walls()
        self.remove_sprites()
        self.add_sprites()
        self.create_walls()
        self.score = 0
        self.game_status = 0
        
    #draw all surfaces on screen
    def draw_surfaces(self):
        for s in self.surfaces:
            self.win.blit(s.surf1, s.rect)
    
    #update all sprite positions
    def update_sprite_pos(self):
        pressed_key = pygame.key.get_pressed()
        self.smoke.update()
        if self.player.update(pressed_key) == 1:
            self.add_smoke()
        self.walls.update()
        
    #main game function
    def update(self):
        self.win.fill(self.win_rgb)
        #self.text.update_text(self.game_status)
        if self.game_status == 0:
            self.draw_surfaces()
            self.update_sprite_pos()
            self.wall_out_bounds()
            self.check_for_collisions()
            self.add_point()
            self.text.update_text(0)
        else:
            self.draw_surfaces()
            self.update_sprite_pos()
            self.text.update_text(1)
        pygame.display.flip()
        self.clock.tick_busy_loop(self.clock_speed) 

    def add_smoke(self):
        rand_x = random.randint(-5, 5)
        rand_y = random.randint(-5, 5)
        smoke = sprite_classes.Smoke(self.width, self.height, [self.player.get_center_x() + rand_x, self.player.get_center_y() + 25 + rand_y], "images/smoke.png")
        self.smoke.add(smoke)
        self.surfaces.add(smoke)

    def add_wall(self, centerx):
        centerx = centerx
        top_rand_int = random.randint(250, 850)
        centery = self.height / 2 - top_rand_int
        if centery + 100 > self.last_bottom:
            centery = self.last_bottom - 200
        wall = sprite_classes.Wall(self.width, self.height, [centerx, centery], "images\wall.png")
        self.top_walls.add(wall)
        self.walls.add(wall)
        self.surfaces.add(wall)
        b = 800 - (970 - top_rand_int)
        a = centery + 970 + 50
        centery = random.randint(a, a + b)
        if centery - 100 < self.last_top:
            centery = self.last_top + 200
        wall = sprite_classes.Wall(self.width, self.height, [centerx, centery], "images\wall.png")
        self.bottom_walls.add(wall)
        self.walls.add(wall)
        self.surfaces.add(wall)
        self.last_top = self.height / 2 - top_rand_int + 970
        self.last_bottom = centery - 970

    def add_player(self):
        self.player = sprite_classes.Player(self.width, self.height, self.player_start)
        self.surfaces.add(self.player)

    def add_sprites(self):
        self.surfaces.add(self.background)
        self.add_player()

    def remove_walls(self):
        for wall in self.walls:
            wall.kill()

    def add_point(self):
        for wall in self.top_walls:
            if wall.get_center_x() + 48 <= self.player_start[0] and wall.get_score_flag() == 0:
                self.text.set_score(self.text.get_score() + 1)
                wall.set_score_flag(1)
        self.text.update_score()

    def wall_out_bounds(self):
        for wall in self.top_walls:
            if wall.get_center_x() - 48 <= 0 and wall.get_flag() == 0:
                self.add_wall(self.width + 95)
                wall.set_flag(1)
            if wall.get_center_x() + 48 <= 0:
                wall.kill()

    def wall_collisions(self):
        collision = pygame.sprite.spritecollideany(self.player, self.walls, collided=pygame.sprite.collide_mask)
        if collision != None:
            self.player.kill()
            self.game_status = 1

    def check_for_collisions(self):
        self.wall_collisions()

#functions for high score
    def read_high_score(self):
        high_score_file = open('./high_score.txt', "r")
        self.text.set_high_score(int(high_score_file.read()))
        high_score_file.close()

    def write_high_score(self):
        high_score_file = open('./high_score.txt', "w")
        high_score_file.write(str(self.text.get_high_score()))
        high_score_file.close()
#ai learns to play my game
#game to learn neat and practice python
import pygame
from game_classes import Game
from pygame.constants import K_RETURN, MOUSEBUTTONDOWN, K_ESCAPE, KEYDOWN #buttons used in game
from constants import *
#calculate point where its going to be next
#then take the current point and create a line or multiple points to next point
#use the collision point of this line or points to determine where ball would collide
 
pygame.init()
win = pygame.display.set_mode((WIDTH, HEIGHT)) #creates a game window with given size 

def main():
    running = True
    game = Game(60, COLOR_WHITE, win, WIDTH, HEIGHT)
    game.start()
    while running:
        for event in pygame.event.get():
            if event.type == KEYDOWN: #exit game if esc key pressed
                if event.key == K_ESCAPE: 
                    game.write_high_score()
                    running = False
                if event.key == K_RETURN:
                    game.restart()
            elif event.type == pygame.QUIT:
                game.write_high_score()
                running = False
        game.update()  
    pygame.quit()

if __name__ == "__main__":
    main()
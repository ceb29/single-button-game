#single button game
#press space to boost up
#avoid the walls
import pygame
from game_classes import Game
from pygame.constants import K_RETURN, MOUSEBUTTONDOWN, K_ESCAPE, KEYDOWN #buttons used in game
from constants import *

pygame.init()
win = pygame.display.set_mode((WIDTH, HEIGHT)) #creates a game window with given size 

def main():
    running = True
    game = Game(60, COLOR_WHITE, win, WIDTH, HEIGHT)
    game.start() #start the main game
    while running:
        for event in pygame.event.get():
            if event.type == KEYDOWN: #exit game if esc key pressed
                if event.key == K_ESCAPE: 
                    game.write_high_score() #save the current high score
                    running = False
                if event.key == K_RETURN: #restart game if enter is pressed
                    game.restart()
            elif event.type == pygame.QUIT: #exit game if windows closed
                game.write_high_score()
                running = False
        game.update() #keep updating the main game
    pygame.quit()

if __name__ == "__main__":
    main()
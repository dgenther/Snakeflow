import pygame as pg
from game import Game
from snake import vec2

pg.init()

game = Game()
game.run_game_loop()

pg.quit()
quit()
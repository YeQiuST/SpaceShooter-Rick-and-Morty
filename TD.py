import pygame
from tilemap import *
import pytmx
from pytmx.util_pygame import load_pygame
#installer pytmx

# initialize pygame
pygame.init()
clock = pygame.time.Clock()

# create game display
game_display = pygame.display.set_mode((800, 800))
pygame.display.set_caption("Collision detection with Tiled and pytmx")
pytmx_map = load_pygame("test.tmx")
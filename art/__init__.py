import pygame
import utilities

pygame.init()
pygame.display.set_mode([0, 0])

selected_tile_image = pygame.image.load("art/tiles/selected.png")
selected_tile_image.set_colorkey(utilities.colors.key)

bar_size_1 = pygame.image.load("art/bars/1.png")
bar_size_2 = pygame.image.load("art/bars/2.png")
bar_size_3 = pygame.image.load("art/bars/3.png")
bar_size_4 = pygame.image.load("art/bars/4.png")
bar_size_5 = pygame.image.load("art/bars/5.png")
bar_size_6 = pygame.image.load("art/bars/6.png")
bar_size_7 = pygame.image.load("art/bars/7.png")
bar_size_8 = pygame.image.load("art/bars/8.png")
bar_size_9 = pygame.image.load("art/bars/9.png")
bar_images = [bar_size_1,
              bar_size_2,
              bar_size_3,
              bar_size_4,
              bar_size_5,
              bar_size_6,
              bar_size_7,
              bar_size_8,
              bar_size_9]

for each in bar_images:
    each.set_colorkey(utilities.colors.key)

import pygame
from game_tile import GameTile
import utilities
import queue


class Background(pygame.sprite.Sprite):
    def __init__(self, width, height):
        super().__init__()
        self.image = pygame.Surface([width * 40, height * 15])
        self.image.fill(utilities.colors.key)
        self.rect = self.image.get_rect()


class Map(object):
    def __init__(self, dimensions, screen_dimensions):
        self.background = None
        self.screen_dimensions = screen_dimensions
        self.width = dimensions[0]
        self.height = dimensions[1]
        self.number_of_columns = dimensions[0]
        self.number_of_rows = dimensions[1]
        self.game_tile_rows = []
        self.bars = []
        self.x_shift = 0
        self.y_shift = 0

    def map_generation(self):
        tile_width = 40
        tile_height = 15
        grass_1 = pygame.image.load("art/tiles/grass.png").convert()
        grass_1.set_colorkey(utilities.colors.key)
        self.game_tile_rows = []
        self.background = Background(self.width, self.height)

        for y_row in range(self.number_of_rows):
            this_row = []
            for x_column in range(self.number_of_columns):
                new_tile_image = grass_1
                x = ((self.width * tile_width) / 2) - 20 + (x_column - y_row) * 20
                y = (x_column + y_row) * 7
                this_row.append(GameTile(x_column, y_row))
                self.background.image.blit(new_tile_image, (x, y))
            self.game_tile_rows.append(this_row)
        self.background.image.set_colorkey(utilities.colors.key)

    def world_scroll(self, shift_x, shift_y, screen_width, screen_height):
        background_width = self.background.image.get_width()
        background_height = self.background.image.get_height()
        self.x_shift += shift_x
        self.y_shift += shift_y
        if self.y_shift < -(background_height - 40):
            self.y_shift = -(background_height - 40)
        elif self.y_shift > screen_height + -40:
            self.y_shift = screen_height + -40
        if self.x_shift < -(background_width - 40):
            self.x_shift = -(background_width - 40)
        if self.x_shift > screen_width + -40:
            self.x_shift = screen_width + -40

    def draw_to_screen(self, screen):
        background_x_middle = self.background.rect.left + (self.background.image.get_width()) / 2
        objects_to_draw = queue.PriorityQueue()
        for each in self.bars:
            screen_coordinates = utilities.get_screen_coords(each.tile_x,
                                                             each.tile_y,
                                                             self.x_shift,
                                                             self.y_shift,
                                                             self.background.rect.top,
                                                             background_x_middle)
            objects_to_draw.put((screen_coordinates[1], screen_coordinates[0], each))

        while not objects_to_draw.empty():
            y, x, bar = objects_to_draw.get()
            screen.blit(bar.sprite.image, [(x + self.x_shift),
                                           (y - 86 + self.y_shift)])


import pygame
from game_tile import GameTile
import utilities


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
        self.x_shift += shift_x
        self.y_shift += shift_y
        if self.x_shift > 0:
            self.x_shift = 0
        elif self.x_shift < -(self.width - screen_width) and self.width > screen_width:
            self.x_shift = -(self.width - screen_width)
        if self.y_shift > 0:
            self.y_shift = 0
        elif self.y_shift < -(self.height - screen_height + 80) and self.height > screen_height:
            self.y_shift = -(self.height - screen_height + 80)

    def draw_to_screen(self, screen):
        background_x_middle = self.background.rect.left + (self.background.image.get_width()) / 2

        for each in self.bars:
            screen_coordinates = utilities.get_screen_coords(each.tile_x,
                                                             each.tile_y,
                                                             self.x_shift,
                                                             self.y_shift,
                                                             self.background.rect.top,
                                                             background_x_middle)
            screen.blit(each.sprite.image, [screen_coordinates[0] + self.x_shift, screen_coordinates[1] - 86 + self.y_shift])

    def y_based_draw_to_screen(self, screen):
        background_x_middle = self.background.rect.left + (self.background.image.get_width()) / 2
        objects_to_draw = {}
        for number in range(1000):
            objects_to_draw[number] = []

        for each in self.bars:
            for each in self.bars:
                screen_coordinates = utilities.get_screen_coords(each.tile_x,
                                                                 each.tile_y,
                                                                 self.x_shift,
                                                                 self.y_shift,
                                                                 self.background.rect.top,
                                                                 background_x_middle)
            objects_to_draw[screen_coordinates[1]].append(each)
        rows_to_draw = []
        for y_level in range(self.background.rect.bottom - self.background.rect.top):
            this_row = []
            for key in objects_to_draw:
                if key == y_level:
                    this_row = (objects_to_draw[key])
            rows_to_draw.append(this_row)

        for row in rows_to_draw:
            for entity in row:
                screen_coordinates = utilities.get_screen_coords(each.tile_x,
                                                                 each.tile_y,
                                                                 self.x_shift,
                                                                 self.y_shift,
                                                                 self.background.rect.top,
                                                                 background_x_middle)
                screen.blit(entity.sprite.image, [(screen_coordinates[0] + self.x_shift),
                                                  (screen_coordinates[1] - 86 + self.y_shift)])


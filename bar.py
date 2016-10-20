import pygame
import art
import utilities
import random


class Bar(object):
    def __init__(self, x, y, size, game_map):
        self.tile_x = x
        self.tile_y = y
        self.size = size
        self.sprite = pygame.sprite.Sprite()
        self.set_image()
        self.game_map = game_map
        game_map.bars.append(self)
        game_map.game_tile_rows[y][x].bar = self
        self.food_bar = 0
        self.neighbor_count = 0

    def set_image(self):
        self.sprite.image = art.bar_images[self.size - 1]
        self.sprite.rect = self.sprite.image.get_rect()

    def tick_cycle(self, game_map):
        neighbor_count = 0
        sum_neighbor_count = 1
        neighbor_tiles = utilities.get_adjacent_tiles(game_map.game_tile_rows[self.tile_y][self.tile_x],
                                                      game_map)
        open_neighbor_tiles = []
        for each in neighbor_tiles:
            open_neighbor_tiles.append(each)
        for each in neighbor_tiles:
            if each.bar:
                open_neighbor_tiles.remove(each)
                if each.bar != self:
                    neighbor_count += 1
                sum_neighbor_count += each.bar.neighbor_count
        self.neighbor_count = neighbor_count
        self.food_bar += sum_neighbor_count

        if self.food_bar >= self.size * self.size * 1000:
            self.food_bar = 0
            if len(open_neighbor_tiles) > 0:
                growth_tile = random.choice(open_neighbor_tiles)
                Bar(growth_tile.column, growth_tile.row, 1, game_map)
            else:
                if self.size < 9:
                    self.size += 1
                    self.set_image()

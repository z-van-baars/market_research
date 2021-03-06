import pygame
import utilities
from utilities import GameState
import game_map
from bar import Bar
import random
import art

pygame.init()
pygame.display.set_mode([0, 0])


def do_nothing(game_state):
    pass


def up_key(game_state):
    game_state.active_map.world_scroll(0,
                                       20,
                                       game_state.screen_width,
                                       game_state.screen_height)


def down_key(game_state):
    game_state.active_map.world_scroll(0,
                                       -20,
                                       game_state.screen_width,
                                       game_state.screen_height)


def left_key(game_state):
    game_state.active_map.world_scroll(20,
                                       0,
                                       game_state.screen_width,
                                       game_state.screen_height)


def right_key(game_state):
    game_state.active_map.world_scroll(-20,
                                       0,
                                       game_state.screen_width,
                                       game_state.screen_height)


key_functions = {pygame.K_UP: up_key,
                 pygame.K_DOWN: down_key,
                 pygame.K_LEFT: left_key,
                 pygame.K_RIGHT: right_key}


def main(game_state):
    tiny_font = pygame.font.SysFont('Calibri', 11, True, False)
    message = tiny_font.render("Market Research Time!", True, utilities.colors.white)
    done = False

    Bar(4, 4, 1, game_state.active_map)
    background_width = game_state.active_map.background.image.get_width()
    background_height = game_state.active_map.background.image.get_height()
    game_state.active_map.x_shift = game_state.screen_width / 2 - background_width / 2
    game_state.active_map.y_shift = game_state.screen_height / 2 - (background_height / 2)

    while not done:
        population = 0
        background_left = 0
        background_left += game_state.active_map.x_shift
        background_top = 0
        background_top += game_state.active_map.y_shift
        background_x_middle = background_left + background_width / 2
        background_bottom = background_top + background_height
        background_right = background_left + background_width
        mouse_pos = pygame.mouse.get_pos()
        map_xy = utilities.get_map_coords(game_state.active_map.x_shift,
                                          game_state.active_map.y_shift,
                                          mouse_pos,
                                          background_left,
                                          background_top,
                                          background_x_middle)
        selected_tile = None
        if 0 <= map_xy[0] <= len(game_state.active_map.game_tile_rows[0]) - 1 and 0 <= map_xy[1] <= len(game_state.active_map.game_tile_rows) - 1:
            selected_tile = game_state.active_map.game_tile_rows[map_xy[1]][map_xy[0]]
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if utilities.check_if_inside(background_left,
                                             background_right,
                                             background_top,
                                             background_bottom,
                                             mouse_pos):
                    if selected_tile is not None and selected_tile.bar is None:
                        Bar(map_xy[0], map_xy[1], 1, game_state.active_map)
            elif event.type == pygame.KEYDOWN:
                key_functions.get(event.key, do_nothing)(game_state)

        for each in game_state.active_map.bars:
            each.tick_cycle(game_state.active_map)
            population += each.size

        game_state.screen.fill(utilities.colors.background_blue)
        game_state.screen.blit(game_state.active_map.background.image, [background_left,
                                                                        background_top])
        if selected_tile is not None:
            selected_coords = utilities.get_screen_coords(selected_tile.column,
                                                          selected_tile.row,
                                                          game_state.active_map.x_shift,
                                                          game_state.active_map.y_shift,
                                                          background_top,
                                                          background_x_middle)
            game_state.screen.blit(art.selected_tile_image, [selected_coords[0], selected_coords[1]])

        game_state.active_map.draw_to_screen(game_state.screen)

        population_stamp = tiny_font.render("Pop:{0}".format(population), True, utilities.colors.white)
        mouse_stamp = tiny_font.render("{0}".format(mouse_pos), True, utilities.colors.white)

        game_state.screen.blit(message, [game_state.screen_width / 2 - (message.get_width() / 2),
                                         2])
        game_state.screen.blit(population_stamp, [2, 2])
        game_state.screen.blit(mouse_stamp, [2, 14])

        pygame.display.flip()
        game_state.clock.tick(60)
        game_state.time += 1


game_state = GameState(1000, 600)
game_state.active_map = game_map.Map((20, 20), (game_state.screen_width, game_state.screen_height))
game_state.active_map.map_generation()
main(game_state)

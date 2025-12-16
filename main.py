import pygame, sys
from config import *
import game_state as gs
from screens import *
from draw import draw_game
from input_handler import handle_mouse_down

running = True

while running:

    if gs.state == START_SCREEN:
        draw_start_screen()
    elif gs.state == LOSE_SCREEN:
        draw_lose_screen()
    else:
        draw_game()

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            handle_mouse_down(event.pos)

from config import WIN, FONT, BIG, WIDTH
from cards import calc_best_total
import game_state as gs
from buttons import *

def draw_text(text, x, y, font=FONT):
    WIN.blit(font.render(text, True, (255,255,255)), (x,y))

def draw_centered(text, y, font=BIG):
    surf = font.render(text, True, (255,255,255))
    WIN.blit(surf, ((WIDTH - surf.get_width())//2, y))

def draw_card(card, x, y):
    import pygame
    pygame.draw.rect(WIN, (30,60,120), (x,y,70,100), border_radius=8)
    label = FONT.render(f"{card['rank']}{card['suit']}", True, (255,255,255))
    WIN.blit(label, (x+10, y+35))

    draw_text(f"Dealer Mode: {gs.dealer_mode}", WIDTH - 300, 20)

def draw_game():
    WIN.fill((30,30,30))
    draw_text(f"Balance: ${gs.balance}", 20, 20)
    draw_text(f"Wins: {gs.wins}", 20, 50)
    draw_text(f"Rounds: {gs.rounds}", 20, 80)
    draw_text(f"Bet: ${gs.bet}", 20, 110)

    if gs.round_active:
        hit_btn.draw()
        stand_btn.draw()
    if gs.show_newround_button:
        new_btn.draw()
    if gs.can_change_bet:
        bet5_btn.draw(); bet10_btn.draw(); bet20_btn.draw(); bet50_btn.draw()
        mode_normal_btn.draw(); mode_heaven_btn.draw()
        mode_rigged_btn.draw(); mode_impossible_btn.draw(); mode_beginner_btn.draw()

    # -------- PLAYER CARDS --------
    px = 300
    for card in gs.player:
        draw_card(card, px, 450)
        px += 80

    # -------- DEALER CARDS --------
    dx = 300
    for card in gs.dealer:
        draw_card(card, dx, 250)
        dx += 80

    if gs.done:
        draw_centered(gs.message, 380, FONT)

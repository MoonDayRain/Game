import random
import game_state as gs
from config import START_SCREEN, GAME, LOSE_SCREEN
from buttons import *
from round_logic import init_round, result_message
from cards import card_value, calc_best_total

def handle_mouse_down(pos):
    mx, my = pos

    # ---------------- START SCREEN ----------------
    if gs.state == START_SCREEN:
        gs.state = GAME
        gs.balance = 100
        gs.wins = 0
        gs.rounds = 0
        return

    # ---------------- LOSE SCREEN ----------------
    if gs.state == LOSE_SCREEN:
        if restart_btn.clicked((mx, my)):
            gs.state = START_SCREEN
            gs.balance = 100
            gs.wins = 0
            gs.rounds = 0
        return

    # ---------------- DEALER MODE ----------------
    if gs.can_change_bet:
        if mode_normal_btn.clicked((mx,my)): gs.dealer_mode = "Normal"
        if mode_heaven_btn.clicked((mx,my)): gs.dealer_mode = "Heaven"
        if mode_rigged_btn.clicked((mx,my)): gs.dealer_mode = "Rigged"
        if mode_impossible_btn.clicked((mx,my)): gs.dealer_mode = "Impossible"
        if mode_beginner_btn.clicked((mx,my)): gs.dealer_mode = "Beginner"

        if bet5_btn.clicked((mx,my)): gs.bet = 5
        if bet10_btn.clicked((mx,my)): gs.bet = 10
        if bet20_btn.clicked((mx,my)): gs.bet = 20
        if bet50_btn.clicked((mx,my)): gs.bet = 50

    # ---------------- NEW ROUND ----------------
    if gs.show_newround_button and new_btn.clicked((mx,my)):
        if gs.balance <= 0:
            gs.state = LOSE_SCREEN
        else:
            init_round()
        return

    # ---------------- HIT ----------------
    if gs.round_active and hit_btn.clicked((mx,my)) and not gs.done:

        if gs.dealer_mode == "Rigged":
            high_cards = [c for c in gs.deck if card_value(c) >= 10]
            if high_cards and random.random() < 0.40:
                card = random.choice(high_cards)
                gs.deck.remove(card)
                gs.player.append(card)
            else:
                gs.player.append(gs.deck.pop())
        else:
            gs.player.append(gs.deck.pop())

        if calc_best_total(gs.player) > 21:
            gs.done = True
            gs.message = result_message()
        return

    # ---------------- STAND ----------------
    if gs.round_active and stand_btn.clicked((mx, my)) and not gs.done:

        if gs.dealer_mode == "Impossible":
            # Force dealer to EXACTLY 21
            while calc_best_total(gs.dealer) < 21 and gs.deck:
                needed = 21 - calc_best_total(gs.dealer)

                # cards that finish exactly at 21
                exact_cards = [
                    c for c in gs.deck
                    if card_value(c) == needed or
                    (c['rank'] == 'A' and needed in (1, 11))
                ]

                if exact_cards:
                    card = random.choice(exact_cards)
                    gs.deck.remove(card)
                    gs.dealer.append(card)
                    break  # we hit 21 exactly
                else:
                    # fallback: safe card that won't bust
                    safe_cards = [
                        c for c in gs.deck
                        if calc_best_total(gs.dealer + [c]) <= 21
                    ]
                    if not safe_cards:
                        break
                    card = random.choice(safe_cards)
                    gs.deck.remove(card)
                    gs.dealer.append(card)

        else:
            while calc_best_total(gs.dealer) < 17:
                gs.dealer.append(gs.deck.pop())

        gs.done = True
        gs.message = result_message()

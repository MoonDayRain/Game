import pygame
import random
import sys

pygame.init()
pygame.font.init()

# ------------------- DISPLAY -------------------
WIDTH, HEIGHT = 800, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Blackjack (Pygame)")

FONT = pygame.font.SysFont("arial", 26)
BIG = pygame.font.SysFont("arial", 55)

# ------------------- GAME STATE -------------------
balance = 100
wins = 0
rounds = 0
bet = 10

player = []
dealer = []
deck = []
done = False
message = "Press SPACE to start"

# GAME MODES
START_SCREEN = 0
GAME = 1
LOSE_SCREEN = 2

state = START_SCREEN


# ------------------- CARD LOGIC -------------------
def new_deck():
    ranks = ['2','3','4','5','6','7','8','9','10','J','Q','K','A']
    suits = ['♠','♥','♦','♣']
    deck = [{'rank': r, 'suit': s} for r in ranks for s in suits]
    random.shuffle(deck)
    return deck

def card_value(card):
    if card['rank'] in ['J','Q','K']:
        return 10
    if card['rank'] == 'A':
        return 11
    return int(card['rank'])

def calc_best_total(hand):
    total = sum(card_value(c) for c in hand)
    aces = sum(1 for c in hand if c['rank'] == 'A')
    while total > 21 and aces:
        total -= 10
        aces -= 1
    return total


# ------------------- ROUND MANAGEMENT -------------------
def init_round():
    global deck, player, dealer, done, rounds

    deck = new_deck()
    player = [deck.pop(), deck.pop()]
    dealer = [deck.pop(), deck.pop()]
    done = False
    rounds += 1


def result_message():
    global balance, wins

    p = calc_best_total(player)
    d = calc_best_total(dealer)

    # Player bust
    if p > 21:
        balance -= bet
        return f"You busted! Dealer wins. -${bet}"

    # Dealer bust
    if d > 21:
        balance += bet
        wins += 1
        return f"Dealer busted — You win! +${bet}"

    # Player blackjack
    if p == 21 and len(player) == 2:
        bonus = int(bet * 1.5)
        balance += bonus
        wins += 1
        return f"BLACKJACK! +${bonus}"

    # Dealer blackjack
    if d == 21 and len(dealer) == 2:
        balance -= bet
        return f"Dealer Blackjack. -${bet}"

    # Tie
    if p == d:
        return "Push (tie)."

    # Win or Lose
    if p > d:
        balance += bet
        wins += 1
        return f"You win! +${bet}"
    else:
        balance -= bet
        return f"Dealer wins. -${bet}"


# ------------------- DRAW FUNCTIONS -------------------
def draw_text(text, x, y, font=FONT, color=(255,255,255)):
    WIN.blit(font.render(text, True, color), (x, y))

def draw_centered(text, y, font=BIG, color=(255,255,255)):
    surf = font.render(text, True, color)
    WIN.blit(surf, ((WIDTH - surf.get_width()) // 2, y))

def draw_card(card, x, y):
    pygame.draw.rect(WIN, (30, 60, 120), (x, y, 70, 100), border_radius=8)
    label = FONT.render(f"{card['rank']}{card['suit']}", True, (255,255,255))
    WIN.blit(label, (x + 10, y + 35))


def draw_start_screen():
    WIN.fill((10, 10, 10))
    draw_centered("BLACKJACK", 180)
    draw_centered("Press SPACE to Start", 320, FONT)
    pygame.display.update()


def draw_lose_screen():
    WIN.fill((40, 0, 0))
    draw_centered("YOU LOST ALL YOUR MONEY", 180)
    draw_centered("Press R to Restart", 300, FONT)
    draw_centered("Press Q to Quit", 350, FONT)
    pygame.display.update()


def draw_game():
    WIN.fill((20, 20, 20))

    # Stats
    draw_text(f"Balance: ${balance}", 20, 20)
    draw_text(f"Wins: {wins}", 20, 50)
    draw_text(f"Rounds: {rounds}", 20, 80)
    draw_text(f"Bet: ${bet}", 20, 110)

    # Dealer
    draw_text("Dealer", 350, 20)
    x = 260
    for i, c in enumerate(dealer):
        if i == 1 and not done:
            pygame.draw.rect(WIN, (80,80,80), (x,150,70,100), border_radius=8)
            draw_text("?", x+25, 185)
        else:
            draw_card(c, x, 150)
        x += 80

    draw_text(f"Total: {calc_best_total(dealer) if done else '??'}", 365, 260)

    # Player
    draw_text("You", 370, 300)
    x = 260
    for c in player:
        draw_card(c, x, 350)
        x += 80

    draw_text(f"Total: {calc_best_total(player)}", 365, 460)

    # Message
    draw_centered(message, 520, FONT)

    # Controls
    draw_centered("Controls: N=new | H=hit | S=stand | 1=$5 | 2=$10 | 3=$20 | 4=$50", 560, FONT)

    pygame.display.update()


# ------------------- MAIN LOOP -------------------
running = True

while running:

    if state == START_SCREEN:
        draw_start_screen()

    elif state == LOSE_SCREEN:
        draw_lose_screen()

    else:
        draw_game()

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:

            # ESC to quit
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

            # ---------------- START SCREEN ----------------
            if state == START_SCREEN:
                if event.key == pygame.K_SPACE:
                    state = GAME
                    balance = 100
                    wins = 0
                    rounds = 0
                    message = "Press N to start"
                continue

            # ---------------- LOSE SCREEN ----------------
            if state == LOSE_SCREEN:
                if event.key == pygame.K_r:   # Restart
                    state = START_SCREEN
                if event.key == pygame.K_q:   # Quit
                    pygame.quit()
                    sys.exit()
                continue

            # ---------------- GAME SCREEN ----------------

            # Betting
            if event.key == pygame.K_1: bet = 5
            if event.key == pygame.K_2: bet = 10
            if event.key == pygame.K_3: bet = 20
            if event.key == pygame.K_4: bet = 50

            # New round
            if event.key == pygame.K_n:
                if balance <= 0:
                    state = LOSE_SCREEN
                else:
                    init_round()
                    message = f"New round — Bet: ${bet}"

            # Hit
            if event.key == pygame.K_h and not done and player:
                player.append(deck.pop())
                if calc_best_total(player) > 21:
                    done = True
                    message = result_message()
                    if balance <= 0:
                        state = LOSE_SCREEN

            # Stand
            if event.key == pygame.K_s and not done and player:
                while calc_best_total(dealer) < 17:
                    dealer.append(deck.pop())
                done = True
                message = result_message()
                if balance <= 0:
                    state = LOSE_SCREEN

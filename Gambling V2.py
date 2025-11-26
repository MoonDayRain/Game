import pygame
import random
import sys

pygame.init()
pygame.font.init()

# ------------------- DISPLAY -------------------
WIDTH, HEIGHT = 1280, 720
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
message = "Press NEW ROUND to start"

can_change_bet = True
show_newround_button = True   # <<< NEW FLAG

# GAME STATES
GAME = 1
LOSE_SCREEN = 2
START_SCREEN = 0

state = START_SCREEN

# ------------------- BUTTON SYSTEM -------------------
class Button:
    def __init__(self, x, y, w, h, text):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text

    def draw(self):
        pygame.draw.rect(WIN, (70, 70, 70), self.rect, border_radius=8)
        pygame.draw.rect(WIN, (200, 200, 200), self.rect, 2, border_radius=8)
        txt = FONT.render(self.text, True, (255,255,255))
        WIN.blit(txt, (self.rect.x + (self.rect.width - txt.get_width())//2,
                    self.rect.y + (self.rect.height - txt.get_height())//2))

    def clicked(self, pos):
        return self.rect.collidepoint(pos)

# ------------------- BUTTONS -------------------
centerX = WIDTH // 2

# HIT / STAND centered below the cards
hit_btn = Button(centerX - 200, 600, 150, 55, "HIT")
stand_btn = Button(centerX + 50, 600, 150, 55, "STAND")

# NEW ROUND centered between them
new_btn = Button(centerX - 75, 540, 150, 55, "NEW ROUND")

# BET buttons moved to right side (still consistent with 720p layout)
bet5_btn = Button(WIDTH - 180, 350, 120, 50, "$5")
bet10_btn = Button(WIDTH - 180, 410, 120, 50, "$10")
bet20_btn = Button(WIDTH - 180, 470, 120, 50, "$20")
bet50_btn = Button(WIDTH - 180, 530, 120, 50, "$50")

# Restart screen button centered
restart_btn = Button(centerX - 100, 500, 200, 70, "RESTART")

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
    global deck, player, dealer, done, rounds, can_change_bet, message, show_newround_button

    deck = new_deck()
    player = [deck.pop(), deck.pop()]
    dealer = [deck.pop(), deck.pop()]
    done = False
    rounds += 1
    can_change_bet = False
    show_newround_button = False    # <<< HIDE IT ON ROUND START
    message = f"Bet locked: ${bet}"

def result_message():
    global balance, wins, can_change_bet, show_newround_button

    p = calc_best_total(player)
    d = calc_best_total(dealer)

    # round ends -> show NEW ROUND button again
    show_newround_button = True

    if p > 21:
        balance -= bet
        can_change_bet = True
        return f"You busted! Dealer wins. -${bet}"

    if d > 21:
        balance += bet
        wins += 1
        can_change_bet = True
        return f"Dealer busted — You win! +${bet}"

    if p == 21 and len(player) == 2:
        bonus = int(bet * 1.5)
        balance += bonus
        wins += 1
        can_change_bet = True
        return f"BLACKJACK! +${bonus}"

    if d == 21 and len(dealer) == 2:
        balance -= bet
        can_change_bet = True
        return f"Dealer Blackjack. -${bet}"

    if p == d:
        can_change_bet = True
        return "Push (tie)."

    if p > d:
        balance += bet
        wins += 1
        can_change_bet = True
        return f"You win! +${bet}"

    balance -= bet
    can_change_bet = True
    return f"Dealer wins. -${bet}"

# ------------------- DRAW FUNCTIONS -------------------
def draw_text(text, x, y, font=FONT, color=(255,255,255)):
    WIN.blit(font.render(text, True, color), (x, y))

def draw_centered(text, y, font=BIG):
    surf = font.render(text, True, (255,255,255))
    WIN.blit(surf, ((WIDTH - surf.get_width()) // 2, y))

def draw_card(card, x, y):
    pygame.draw.rect(WIN, (30, 60, 120), (x, y, 70, 100), border_radius=8)
    label = FONT.render(f"{card['rank']}{card['suit']}", True, (255,255,255))
    WIN.blit(label, (x + 10, y + 35))

def draw_game():
    WIN.fill((30, 30, 30))

    draw_text(f"Balance: ${balance}", 20, 20)
    draw_text(f"Wins: {wins}", 20, 50)
    draw_text(f"Rounds: {rounds}", 20, 80)
    draw_text(f"Bet: ${bet}", 20, 110)

    draw_text("Dealer", 350, 20)
    x = centerX - 160

    for i, c in enumerate(dealer):
        if i == 1 and not done:
            pygame.draw.rect(WIN, (80,80,80), (x,150,70,100), border_radius=8)
            draw_text("?", x+25, 185)
        else:
            draw_card(c, x, 150)
        x += 90



    draw_text(f"Total: {calc_best_total(dealer) if done else '??'}", 365, 260)

    draw_text("You", 370, 300)
    x = centerX - 160
    for c in player:
        draw_card(c, x, 350)
        x += 90

    draw_text(f"Total: {calc_best_total(player)}", 365, 460)

    draw_centered(message, 670, FONT)

    hit_btn.draw()
    stand_btn.draw()

    # <<< NEW ROUND BUTTON ONLY IF ROUND ENDED
    if show_newround_button:
        new_btn.draw()

    if can_change_bet:
        bet5_btn.draw()
        bet10_btn.draw()
        bet20_btn.draw()
        bet50_btn.draw()

    pygame.display.update()

def draw_start_screen():
    WIN.fill((0,0,0))
    draw_centered("BLACKJACK", 200)
    draw_centered("Click to Start", 330, FONT)
    pygame.display.update()

def draw_lose_screen():
    WIN.fill((60,0,0))
    draw_centered("YOU LOST ALL YOUR MONEY", 200)
    draw_centered("Click RESTART to play again", 300, FONT)
    restart_btn.draw()
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

        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = event.pos

            # START → GAME
            if state == START_SCREEN:
                state = GAME
                balance = 100
                wins = 0
                rounds = 0
                continue

            # LOSE SCREEN
            if state == LOSE_SCREEN:
                if restart_btn.clicked((mx,my)):
                    state = START_SCREEN
                    balance = 100
                    wins = 0
                    rounds = 0
                continue

            # BETTING
            if can_change_bet:
                if bet5_btn.clicked((mx,my)): bet = 5
                if bet10_btn.clicked((mx,my)): bet = 10
                if bet20_btn.clicked((mx,my)): bet = 20
                if bet50_btn.clicked((mx,my)): bet = 50

            # NEW ROUND BUTTON
            if show_newround_button and new_btn.clicked((mx,my)):
                if balance <= 0:
                    state = LOSE_SCREEN
                else:
                    init_round()

            # HIT
            if hit_btn.clicked((mx,my)) and not done and not can_change_bet:
                player.append(deck.pop())
                if calc_best_total(player) > 21:
                    done = True
                    message = result_message()

            # STAND
            if stand_btn.clicked((mx,my)) and not done and not can_change_bet:
                while calc_best_total(dealer) < 17:
                    dealer.append(deck.pop())
                done = True
                message = result_message()

    if done and balance <= 0:
        state = LOSE_SCREEN

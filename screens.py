from config import WIN, FONT, BIG, WIDTH
from buttons import restart_btn

def draw_centered(text, y, font=BIG):
    surf = font.render(text, True, (255,255,255))
    WIN.blit(surf, ((WIDTH - surf.get_width())//2, y))

def draw_start_screen():
    WIN.fill((0,0,0))
    draw_centered("BLACKJACK", 200)
    draw_centered("Click to Start", 330, FONT)

def draw_lose_screen():
    WIN.fill((60,0,0))
    draw_centered("YOU LOST ALL YOUR MONEY", 200)
    draw_centered("Click RESTART to play again", 300, FONT)
    restart_btn.draw()

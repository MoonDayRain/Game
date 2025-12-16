import pygame
from config import WIN, FONT, WIDTH, HEIGHT

class Button:
    def __init__(self, x, y, w, h, text):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text

    def draw(self):
        pygame.draw.rect(WIN, (70,70,70), self.rect, border_radius=8)
        pygame.draw.rect(WIN, (200,200,200), self.rect, 2, border_radius=8)
        txt = FONT.render(self.text, True, (255,255,255))
        WIN.blit(txt, (
            self.rect.x + (self.rect.width - txt.get_width())//2,
            self.rect.y + (self.rect.height - txt.get_height())//2
        ))

    def clicked(self, pos):
        return self.rect.collidepoint(pos)

centerX = WIDTH // 2

hit_btn = Button(centerX - 200, 600, 150, 55, "HIT")
stand_btn = Button(centerX + 50, 600, 150, 55, "STAND")
new_btn = Button(centerX - 75, 540, 150, 55, "NEW ROUND")

bet5_btn = Button(WIDTH - 180, 350, 120, 50, "$5")
bet10_btn = Button(WIDTH - 180, 410, 120, 50, "$10")
bet20_btn = Button(WIDTH - 180, 470, 120, 50, "$20")
bet50_btn = Button(WIDTH - 180, 530, 120, 50, "$50")

mode_normal_btn = Button(WIDTH - 180, 600, 120, 40, "Normal")
mode_heaven_btn = Button(WIDTH - 180, 645, 120, 40, "Heaven")
mode_rigged_btn = Button(WIDTH - 180, 690, 120, 40, "Rigged")
mode_impossible_btn = Button(WIDTH - 320, 645, 120, 40, "Impossible")
mode_beginner_btn = Button(WIDTH - 320, 600, 120, 40, "Beginner")

restart_btn = Button(centerX - 100, 500, 200, 70, "RESTART")

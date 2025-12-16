import pygame

pygame.init()
pygame.font.init()

WIDTH, HEIGHT = 1280, 720
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Blackjack (Pygame)")

FONT = pygame.font.SysFont("arial", 26)
BIG = pygame.font.SysFont("arial", 55)

START_SCREEN = 0
GAME = 1
LOSE_SCREEN = 2

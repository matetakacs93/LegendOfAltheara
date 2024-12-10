import pygame

class Platform:
    def __init__(self, x, y, width, height, color=(100, 100, 100)):
        """Inicializálja a platformot."""
        self.rect = pygame.Rect(x, y, width, height)  # Platform mérete és pozíciója
        self.color = color  # Platform színe

    def draw(self, screen):
        """Kirajzolja a platformot a képernyőre."""
        pygame.draw.rect(screen, self.color, self.rect)

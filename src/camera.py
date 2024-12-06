import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT

class Camera:
    def __init__(self, level_width, level_height):
        """A kamera inicializálása a pálya szélességével és magasságával."""
        self.camera = pygame.Rect(0, 0, level_width, level_height)  # Kamera területének definiálása
        self.level_width = level_width  # A pálya szélessége
        self.level_height = level_height  # A pálya magassága

    def apply(self, entity):
        """Az entitás pozíciójának beállítása a kamera alapján."""
        return entity.rect.move(self.camera.topleft)  # Az entitás pozíciójának módosítása a kamera nézete szerint

    def update(self, target):
        """A kamera követi a célpontot."""
        x = -target.rect.centerx + SCREEN_WIDTH // 2  # Horizontális pozíció beállítása
        y = -target.rect.centery + SCREEN_HEIGHT // 2  # Vertikális pozíció beállítása

        # Korlátozás a pálya széleihez
        x = min(0, x)  # Bal szélen túl ne mozogjon
        x = max(-(self.level_width - SCREEN_WIDTH), x)  # Jobb szélen túl ne mozogjon
        y = min(0, y)  # Felső szélen túl ne mozogjon
        y = max(-(self.level_height - SCREEN_HEIGHT), y)  # Alsó szélen túl ne mozogjon

        self.camera = pygame.Rect(x, y, self.level_width, self.level_height)  # Kamera frissítése

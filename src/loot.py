import pygame

class Loot(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, image_path, loot_type):
        super().__init__()
        self.image = pygame.image.load(image_path).convert_alpha()  # Kép betöltése
        self.image = pygame.transform.scale(self.image, (width, height))  # Méretezés
        self.rect = self.image.get_rect(topleft=(x, y))  # Pozíció beállítása
        self.loot_type = loot_type  # Loot típusának mentése (pl. 'coin', 'health')

    def draw(self, screen, camera):
        """A loot kirajzolása a képernyőn."""
        screen.blit(self.image, camera.apply(self))  # A loot megjelenítése a kamera alapján

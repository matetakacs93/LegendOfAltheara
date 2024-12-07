import pygame

class Enemy:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 50, 50)  # Ellenség hitbox
        self.health = 50  # Ellenség életerő
        self.is_dead = False  # Halott állapot

    def take_damage(self, amount):
        """Sebzés fogadása."""
        self.health -= amount
        if self.health <= 0:
             print("Enemy defeated!")  # Ellenség legyőzése

    def draw(self, screen, camera):
        adjusted_rect = camera.apply(self)  # Az ellenség pozíciójának módosítása a kamera szerint
        pygame.draw.rect(screen, (255, 0, 0), adjusted_rect)  # Az ellenség ideiglenes kirajzolása
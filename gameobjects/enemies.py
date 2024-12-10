import pygame

class Enemy:
    def __init__(self, x, y):
        self.x = x  # Az ellenség X koordinátája.
        self.y = y  # Az ellenség Y koordinátája.
        self.width = 50  # Ellenség szélessége.
        self.height = 50  # Ellenség magassága.
        self.health = 100  # Ellenség életereje.
        self.posture = 50  # Ellenség posture értéke.
        self.max_posture = 50
        self.rect = pygame.Rect(x, y, 50, 50)  # Ellenség hitbox
        self.health = 50  # Ellenség életerő
        self.is_dead = False  # Halott állapot

    def take_damage(self, amount):
        """Sebzés fogadása."""
        self.health -= amount
        if self.health <= 0:
             print("Enemy defeated!")  # Ellenség legyőzése

    def take_posture_damage(self, amount):
        """
        Posture érték csökkentése az ellenségnél.
        """
        self.posture -= amount
        if self.posture <= 0:
            self.stun()

    def stun(self):
        """
        Stun állapotba kerülés.
        """
        print("Ellenség lebénult!")
        # Lebénulási logika itt...

    def draw(self, screen, camera):
        adjusted_rect = camera.apply(self)  # Az ellenség pozíciójának módosítása a kamera szerint
        pygame.draw.rect(screen, (255, 0, 0), adjusted_rect)  # Az ellenség ideiglenes kirajzolása
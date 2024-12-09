import pygame


class Enemy:
    def __init__(self, x, y, width=50, height=50, health=100, speed=2, aggro_range=200):
        """Ellenség inicializálása."""
        self.x = x  # Ellenség X pozíciója.
        self.y = y  # Ellenség Y pozíciója.
        self.width = width  # Ellenség szélessége.
        self.height = height  # Ellenség magassága.
        self.health = health  # Ellenség életereje.
        self.speed = speed  # Mozgási sebesség.
        self.aggro_range = aggro_range  # Látótávolság.
        self.rect = pygame.Rect(x, y, width, height)  # Hitbox létrehozása.
        self.is_dead = False  # Az ellenség életben van-e.
        self.stunned = False  # Lebénult állapot.
        self.stun_timer = 0  # Lebénulási időzítő.
        self.posture = 50  # Posture érték.
        self.max_posture = 50  # Maximális posture érték.

    def take_damage(self, amount):
        """Az ellenség sebzést szenved el."""
        self.health -= amount  # Életerő csökkentése.
        if self.health <= 0:
            self.is_dead = True  # Ellenség meghal.
            print("Ellenség meghalt!")

    def take_posture_damage(self, amount):
        """Posture sebzést szenved el."""
        self.posture -= amount  # Posture csökkentése.
        if self.posture <= 0:
            self.stun()  # Lebénulás, ha posture eléri a nullát.

    def stun(self):
        """Lebénulási állapot."""
        self.stunned = True  # Lebénulás beállítása.
        self.stun_timer = 2  # Lebénulás időtartama másodpercben.
        print("Ellenség lebénult!")

    def update(self, player, delta_time):
        """Ellenség állapotának frissítése."""
        if self.stunned:  # Ha lebénult, csak az időzítőt csökkentjük.
            self.stun_timer -= delta_time
            if self.stun_timer <= 0:
                self.stunned = False
                self.posture = self.max_posture  # Posture visszaállítása.
            return

        if self.detect_player(player):  # Ha látja a játékost.
            self.chase_player(player)  # Követi a játékost.

    def detect_player(self, player):
        """Vizsgálja, hogy a játékos látótávolságon belül van-e."""
        distance = abs(self.rect.centerx - player.rect.centerx)  # Távolság számítása.
        return distance <= self.aggro_range  # Látótávolság ellenőrzése.

    def chase_player(self, player):
        """A játékos üldözése."""
        if player.rect.centerx < self.rect.centerx:
            self.x -= self.speed  # Balra mozog.
        elif player.rect.centerx > self.rect.centerx:
            self.x += self.speed  # Jobbra mozog.

        self.rect.topleft = (self.x, self.y)  # Hitbox frissítése.

    def draw(self, screen, camera):
        """Ellenség kirajzolása."""
        adjusted_rect = camera.apply(self)  # Kamera által módosított pozíció.
        pygame.draw.rect(screen, (255, 0, 0), adjusted_rect)  # Ellenség kirajzolása piros téglalapként.

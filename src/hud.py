import pygame

class HUD:
    def __init__(self, screen, player):
        self.screen = screen  # A képernyő, ahová rajzoljuk
        self.player = player  # A játékos, akinek az állapotát mutatjuk
        self.font = pygame.font.Font(None, 30)  # Betűtípus az értékekhez

    def draw_health_bar(self):
        """Az életerő sáv megjelenítése."""
        max_width = 200  # Az életerő sáv maximális szélessége
        height = 20  # Az életerő sáv magassága
        x, y = 20, 20  # A sáv pozíciója
        current_width = int(max_width * (self.player.health / self.player.max_health))  # Arányos szélesség

        # Hátteret rajzolunk
        pygame.draw.rect(self.screen, (100, 100, 100), (x, y, max_width, height))
        # Az aktuális életerőt rajzoljuk zöld színnel
        pygame.draw.rect(self.screen, (0, 255, 0), (x, y, current_width, height))

    def draw_xp_bar(self):
        """Az XP sáv megjelenítése."""
        max_width = 200  # Az XP sáv maximális szélessége
        height = 20  # Az XP sáv magassága
        x, y = 20, 50  # A sáv pozíciója
        current_width = int(max_width * (self.player.xp / self.player.xp_needed))  # Arányos szélesség

        # Hátteret rajzolunk
        pygame.draw.rect(self.screen, (100, 100, 100), (x, y, max_width, height))
        # Az aktuális XP-t rajzoljuk kék színnel
        pygame.draw.rect(self.screen, (0, 0, 255), (x, y, current_width, height))

    def draw(self):
        """Az összes HUD elem kirajzolása."""
        self.draw_health_bar()  # Életerő sáv
        self.draw_xp_bar()  # XP sáv


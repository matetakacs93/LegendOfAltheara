import pygame

class LevelUpMenu:
    def __init__(self, screen, player):
        self.screen = screen  # A képernyő, ahová rajzoljuk
        self.player = player  # A játékos, akinek a statisztikáit növeljük
        self.font = pygame.font.Font(None, 36)  # Betűtípus a menühöz
        self.options = ["Health +20", "Attack +5", "Defense +5"]  # Szintlépési opciók
        self.selected_option = 0  # Alapértelmezett kiválasztott opció

    def draw(self):
        """A szintlépési menü megjelenítése."""
        self.screen.fill((50, 50, 50))  # Háttérszín
        title = self.font.render("Level Up! Choose an upgrade:", True, (255, 255, 255))
        self.screen.blit(title, (self.screen.get_width() // 2 - title.get_width() // 2, 100))

        for i, option in enumerate(self.options):
            color = (255, 255, 255) if i == self.selected_option else (150, 150, 150)
            option_text = self.font.render(option, True, color)
            self.screen.blit(option_text, (self.screen.get_width() // 2 - option_text.get_width() // 2, 200 + i * 50))

    def handle_input(self, event):
        """A felhasználói bevitel kezelése."""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:  # Fel navigáció
                self.selected_option = (self.selected_option - 1) % len(self.options)
            elif event.key == pygame.K_DOWN:  # Le navigáció
                self.selected_option = (self.selected_option + 1) % len(self.options)
            elif event.key == pygame.K_RETURN:  # Választás megerősítése
                if self.selected_option == 0:  # Életerő növelése
                    self.player.max_health += 20
                    self.player.health = self.player.max_health
                elif self.selected_option == 1:  # Támadó erő növelése
                    self.player.attack += 5
                elif self.selected_option == 2:  # Védekező erő növelése
                    self.player.defense += 5
                return True  # Szintlépés befejezése
        return False  # Szintlépés folytatása

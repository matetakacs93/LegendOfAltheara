import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT


class Button:
    def __init__(self, x, y, width, height, text, images, action=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.image_normal = images[0]
        self.image_hover = images[1]
        self.image_pressed = images[2]
        self.action = action
        self.state = "normal"

    def update_state(self, mouse_pos, mouse_pressed):
        if self.rect.collidepoint(mouse_pos):
            if mouse_pressed[0]:  # Bal egérgomb lenyomva
                self.state = "pressed"
            else:
                self.state = "hover"
        else:
            self.state = "normal"

    def draw(self, screen, font):
        if self.state == "normal":
            screen.blit(self.image_normal, self.rect.topleft)
        elif self.state == "hover":
            screen.blit(self.image_hover, self.rect.topleft)
        elif self.state == "pressed":
            screen.blit(self.image_pressed, self.rect.topleft)

        text_surface = font.render(self.text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

class MainMenu:
    def __init__(self, screen, has_save=False):
        """Inicializálja a főmenüt."""
        self.screen = screen  # A képernyő objektum
        self.has_save = has_save  # Van-e mentett játék

        # Háttérkép betöltése
        self.original_background = pygame.image.load("assets/main_menu/main_menu.png").convert()
        self.background = pygame.transform.scale(
            self.original_background, (SCREEN_WIDTH, SCREEN_HEIGHT)
        )  # Átméretezés a képernyő méretére

        self.font = pygame.font.Font(None, 48)  # Betűtípus és méret beállítása

        # Gomb állapot képek betöltése
        button_images = [
            pygame.image.load("assets/main_menu/button_normal.png").convert_alpha(),
            pygame.image.load("assets/main_menu/button_hover.png").convert_alpha(),
            pygame.image.load("assets/main_menu/button_pressed.png").convert_alpha()
        ]

        settings_images = [
            pygame.image.load("assets/main_menu/settings_normal.png").convert_alpha(),
            pygame.image.load("assets/main_menu/settings_hover.png").convert_alpha(),
            pygame.image.load("assets/main_menu/settings_pressed.png").convert_alpha()
        ]

        # Gombok inicializálása
        self.new_game_button = Button(
            SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 100, 200, 50,
            "Új játék", button_images, self.start_new_game
        )  # Új játék gomb
        self.continue_button = Button(
            SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2, 200, 50,
            "Folytatás", button_images, self.continue_game
        )  # Folytatás gomb
        self.exit_button = Button(
            SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 100, 200, 50,
            "Kilépés", button_images, self.exit_game
        )  # Kilépés gomb
        self.settings_button = Button(
            20, SCREEN_HEIGHT - 70, 50, 50, "",
            settings_images, self.open_settings
        )  # Beállítások gomb, a bal alsó sarokban

    def start_new_game(self):
        """Új játék indítása."""
        return "new_game"

    def continue_game(self):
        """Mentett játék folytatása."""
        return "continue"

    def open_settings(self):
        """Beállítások megnyitása."""
        return "settings"

    def exit_game(self):
        """Kilépés a játékból."""
        return "exit"

    def handle_event(self, event):
        """Események kezelése."""
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()  # Az egér pozíciója
            if self.new_game_button.rect.collidepoint(mouse_pos):
                return self.new_game_button.action()  # Új játék gomb akció
            elif self.has_save and self.continue_button.rect.collidepoint(mouse_pos):
                return self.continue_button.action()  # Folytatás gomb akció
            elif self.settings_button.rect.collidepoint(mouse_pos):
                return self.settings_button.action()  # Beállítások gomb akció
            elif self.exit_button.rect.collidepoint(mouse_pos):
                return self.exit_button.action()  # Kilépés gomb akció
        return None

    def draw(self):
        """A főmenü kirajzolása."""
        self.screen.blit(self.background, (0, 0))  # Háttér kirajzolása
        self.new_game_button.draw(self.screen, self.font)  # Új játék gomb kirajzolása
        if self.has_save:
            self.continue_button.draw(self.screen, self.font)  # Folytatás gomb kirajzolása, ha van mentés
        self.settings_button.draw(self.screen, self.font)  # Beállítások gomb kirajzolása
        self.exit_button.draw(self.screen, self.font)  # Kilépés gomb kirajzolása

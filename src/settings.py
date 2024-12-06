import pygame

# Monitor felbontásának lekérése
pygame.init()
screen_info = pygame.display.Info()
SCREEN_WIDTH = screen_info.current_w
SCREEN_HEIGHT = screen_info.current_h

# Játék natív felbontása
NATIVE_WIDTH = 1920
NATIVE_HEIGHT = 1080

# Skálázási tényezők kiszámítása
SCALE_X = SCREEN_WIDTH / NATIVE_WIDTH
SCALE_Y = SCREEN_HEIGHT / NATIVE_HEIGHT

BACKGROUND_COLOR = (30, 30, 30)  # Sötét szürke háttérszín

# Színek
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Nyelvi beállítások
LANGUAGES = {
    "en": {
        "menu_new_game": "New Game",
        "menu_settings": "Settings",
        "menu_exit": "Exit",
        "pause_continue": "Continue",
        "pause_settings": "Settings",
        "pause_exit": "Exit to Main Menu"
    },
    "hu": {
        "menu_new_game": "Új játék",
        "menu_settings": "Beállítások",
        "menu_exit": "Kilépés",
        "pause_continue": "Folytatás",
        "pause_settings": "Beállítások",
        "pause_exit": "Kilépés a főmenübe"
    }
}

# Alapértelmezett nyelv
CURRENT_LANGUAGE = "en"

# Alap csempe méret
TILE_SIZE = int(64 * SCALE_X)  # Natív 64x64 csempe méret skálázva

# FPS
FPS = 60




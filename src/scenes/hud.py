import pygame  # Pygame modul importálása a játék elemek kezeléséhez

class ProgressBar:
    """Ez az osztály a játék HUD sávját (pl. életerő, mana, XP) kezeli."""
    def __init__(self, screen, x, y, width, height, color_images, background_image, corners):
        self.screen = screen  # Képernyő, ahol a sávot rajzoljuk
        self.x = x  # Sáv bal felső sarkának X koordinátája
        self.y = y  # Sáv bal felső sarkának Y koordinátája
        self.width = width  # Sáv szélessége
        self.height = height  # Sáv magassága
        self.color_images = color_images  # A különböző színű sávok képei
        self.background_image = background_image  # Háttérsáv képe
        self.corners = corners  # A sarokelemek képei
        self.current_value = 1.0  # A sáv kezdőértéke (100%)

    def set_value(self, value):
        """Beállítja a sáv aktuális értékét 0 és 1 között."""
        self.current_value = max(0, min(value, 1))  # Értéket 0 és 1 közé szorítja

    def draw(self, color_key, value):
        """Kirajzolja a sávot a képernyőre."""
        if color_key not in self.color_images:  # Ellenőrzi, hogy a színkulcs érvényes-e
            raise KeyError(f"Invalid color key: {color_key}")

        self.set_value(value)  # Beállítja az aktuális értéket

        # Háttér sáv kirajzolása
        self.screen.blit(self.background_image, (self.x, self.y))  # Háttér rajzolása

        # Kitöltött sáv szélességének kiszámítása
        filled_width = int(self.current_value * self.width)  # Kitöltött szélesség számítása

        # Kitöltött sáv kirajzolása
        filled_bar = pygame.transform.scale(
            self.color_images[color_key], (filled_width, self.height)
        )  # Kitöltött rész méretezése
        self.screen.blit(filled_bar, (self.x, self.y))  # Kitöltött sáv kirajzolása

        # Bal sarokelem kirajzolása
        left_corner = pygame.transform.scale(
            self.corners[0], (self.corners[0].get_width(), self.height)
        )  # Bal sarokelem méretezése
        self.screen.blit(left_corner, (self.x - left_corner.get_width(), self.y))  # Bal sarokelem pozicionálása

        # Jobb sarokelem kirajzolása
        right_corner = pygame.transform.scale(
            self.corners[1], (self.corners[1].get_width(), self.height)
        )  # Jobb sarokelem méretezése
        self.screen.blit(right_corner, (self.x + self.width, self.y))  # Jobb sarokelem pozicionálása


def initialize_hud(screen):
    """Inicializálja a HUD elemeit (életerő, mana, XP sávok)."""
    # Sávok képeinek betöltése
    red_bar = pygame.image.load("assets/hud/loading_red_full_bar.png").convert_alpha()  # Életerő sáv
    blue_bar = pygame.image.load("assets/hud/loading_blue_full_bar.png").convert_alpha()  # Mana sáv
    green_bar = pygame.image.load("assets/hud/loading_green_full_bar.png").convert_alpha()  # XP sáv

    # Háttér kép betöltése
    background_image = pygame.image.load("assets/hud/loading_bar.png").convert_alpha()  # Sáv háttere

    # Sarokelemek betöltése
    left_corner_red = pygame.image.load("assets/hud/loading_red_corner1.png").convert_alpha()  # Bal sarok (piros)
    right_corner_red = pygame.image.load("assets/hud/loading_red_corner2.png").convert_alpha()  # Jobb sarok (piros)
    left_corner_blue = pygame.image.load("assets/hud/loading_blue_corner1.png").convert_alpha()  # Bal sarok (kék)
    right_corner_blue = pygame.image.load("assets/hud/loading_blue_corner2.png").convert_alpha()  # Jobb sarok (kék)
    left_corner_green = pygame.image.load("assets/hud/loading_green_corner1.png").convert_alpha()  # Bal sarok (zöld)
    right_corner_green = pygame.image.load("assets/hud/loading_green_corner2.png").convert_alpha()  # Jobb sarok (zöld)

    # Életerő sáv inicializálása
    health_bar = ProgressBar(
        screen,
        10,
        10,
        200,
        20,
        {"red": red_bar},
        background_image,
        [left_corner_red, right_corner_red],
    )  # Életerő sáv példányosítása

    # Mana sáv inicializálása
    mana_bar = ProgressBar(
        screen,
        10,
        40,
        200,
        20,
        {"blue": blue_bar},
        background_image,
        [left_corner_blue, right_corner_blue],
    )  # Mana sáv példányosítása

    # XP sáv inicializálása
    xp_bar = ProgressBar(
        screen,
        10,
        70,
        200,
        20,
        {"green": green_bar},
        background_image,
        [left_corner_green, right_corner_green],
    )  # XP sáv példányosítása

    # HUD elemek listája
    return {
        "health_bar": health_bar,  # Életerő sáv
        "mana_bar": mana_bar,  # Mana sáv
        "xp_bar": xp_bar,  # XP sáv
    }

def draw_hud(hud_elements, player):
    """Kirajzolja a HUD elemeit a játékos állapotának megfelelően."""
    # Életerő sáv rajzolása
    hud_elements["health_bar"].draw("red", player.health / player.max_health)  # Életerő sáv kirajzolása

    # Mana sáv rajzolása
    hud_elements["mana_bar"].draw("blue", player.mana / player.max_mana)  # Mana sáv kirajzolása

    # XP sáv rajzolása
    hud_elements["xp_bar"].draw("green", player.xp / player.xp_to_level)  # XP sáv kirajzolása


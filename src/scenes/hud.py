import pygame

class ProgressBar:
    def __init__(self, screen, x, y, max_width, fill_image_path, background_image_path):
        """
        HUD sáv inicializálása.

        :param screen: A képernyő, amire rajzolni kell.
        :param x: A sáv bal felső sarkának X koordinátája.
        :param y: A sáv bal felső sarkának Y koordinátája.
        :param max_width: A sáv maximális szélessége.
        :param fill_image_path: A sáv kitöltéséhez tartozó kép elérési útja.
        :param background_image_path: A sáv háttérképének elérési útja.
        """
        self.screen = screen
        self.x = x
        self.y = y
        self.max_width = max_width
        self.fill_image = pygame.image.load(fill_image_path).convert_alpha()
        self.background_image = pygame.image.load(background_image_path).convert_alpha()
        self.current_value = 1.0  # Alapértelmezett érték (100%)

    def set_value(self, value):
        """
        A sáv aktuális értékének beállítása.

        :param value: Új érték 0 és 1 között (arány).
        """
        self.current_value = max(0, min(value, 1))

    def draw(self):
        """
        A sáv kirajzolása a képernyőre.
        """
        # Háttér kirajzolása
        self.screen.blit(self.background_image, (self.x, self.y))

        # Kitöltött sáv szélességének kiszámítása
        filled_width = int(self.current_value * self.max_width)

        # Kitöltés méretezése és rajzolása
        filled_bar = pygame.transform.scale(self.fill_image, (filled_width, self.background_image.get_height()))
        self.screen.blit(filled_bar, (self.x, self.y))


def initialize_hud(screen):
    """
    HUD elemek inicializálása.

    :param screen: A képernyő, amire a HUD elemeket rajzoljuk.
    :return: Egy szótár a HUD elemekkel.
    """
    health_bar = ProgressBar(
        screen,
        x=10, y=10,  # Pozíció
        max_width=200,
        fill_image_path="assets/hud/health_bar.png",
        background_image_path="assets/hud/health_bg.png",
    )

    mana_bar = ProgressBar(
        screen,
        x=10, y=40,  # Pozíció
        max_width=200,
        fill_image_path="assets/hud/mana_bar.png",
        background_image_path="assets/hud/mana_bg.png",
    )

    xp_bar = ProgressBar(
        screen,
        x=10, y=70,  # Pozíció
        max_width=200,
        fill_image_path="assets/hud/xp_bar.png",
        background_image_path="assets/hud/xp_bg.png",
    )

    return {
        "health_bar": health_bar,
        "mana_bar": mana_bar,
        "xp_bar": xp_bar,
    }

def draw_hud(hud_elements, player):
    """
    A HUD elemek kirajzolása.

    :param hud_elements: A HUD elemek szótára.
    :param player: A játékos, akinek az állapota alapján frissítjük a HUD-ot.
    """
    # Sávok értékének frissítése a játékos állapota alapján
    hud_elements["health_bar"].set_value(player.health / player.max_health)
    hud_elements["mana_bar"].set_value(player.mana / player.max_mana)
    hud_elements["xp_bar"].set_value(player.xp / player.xp_to_level)

    # HUD elemek kirajzolása
    for bar in hud_elements.values():
        bar.draw()




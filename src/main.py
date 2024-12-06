import pygame  # A Pygame könyvtár importálása, amely a játék működéséhez szükséges
from settings import *  # A beállításokat tartalmazó fájl importálása
from player import Player  # A játékos osztály importálása
from game_platform import Platform  # A platform osztály importálása
from camera import Camera  # A kamera osztály importálása
from loot import Loot  # A loot (zsákmány) osztály importálása
from main_menu import MainMenu  # Főképernyő betöltése

pygame.init()  # A Pygame inicializálása
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  # A képernyő méretének beállítása
pygame.display.set_caption("Legend of Altheara")  # A játék ablakának címének beállítása


def start_game(screen):
    """A játék fő indító része, ahol a játékos, platformok, lootok és a kamera inicializálása történik."""
    # Játékos inicializálása
    player = Player(SCREEN_WIDTH // 4, SCREEN_HEIGHT - 300)  # A játékos a képernyő szélén kezd

    # Platformok inicializálása
    platforms = [
        Platform(100, SCREEN_HEIGHT - 100, 300, 50),  # Bal oldali platform
        Platform(500, SCREEN_HEIGHT - 200, 300, 50),  # Középső platform
        Platform(900, SCREEN_HEIGHT - 300, 300, 50),  # Jobb oldali platform
    ]

    # Lootok inicializálása
    loots = pygame.sprite.Group()  # Egy csoport a lootok számára
    loots.add(
        Loot(200, SCREEN_HEIGHT - 150, 27, 27, "assets/loots/coin.png", "coin"),  # Érme loot
        Loot(500, SCREEN_HEIGHT - 250, 32, 32, "assets/loots/pink_stone.png", "health")  # Életerő loot
    )

    # Kamera inicializálása
    camera = Camera(level_width=3000, level_height=2000)  # A kamera a pálya méretéhez igazodik

    # Fő játékkör futási állapot
    running = True
    clock = pygame.time.Clock()  # Az FPS kezeléséhez szükséges óra

    while running:
        delta_time = clock.tick(FPS) / 1000  # Az eltelt idő kiszámítása másodpercben

        # Események kezelése
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Ha az ablakot bezárják
                running = False
            elif event.type == pygame.KEYDOWN:  # Ha egy billentyűt lenyomnak
                if event.key == pygame.K_ESCAPE:  # Ha az ESC gombot lenyomják
                    result = pause_menu(screen)  # Pause menü meghívása
                    if result == "main_menu":  # Ha vissza a főmenübe opciót választják
                        return  # Visszatérés a főmenübe

        # Billentyűk lenyomásának lekérdezése
        keys = pygame.key.get_pressed()

        # Játékos frissítése (hozzáadva a lootokat is)
        player.update(keys, delta_time, platforms, loots)

        # Kamera frissítése a játékos pozíciója alapján
        camera.update(player)

        # Képernyő törlése a háttérszínnel
        screen.fill(BACKGROUND_COLOR)

        # Platformok kirajzolása
        for platform in platforms:
            pygame.draw.rect(screen, (100, 100, 100), camera.apply(platform))

        # Lootok kirajzolása
        for loot in loots:
            loot.draw(screen, camera)

        # Játékos kirajzolása
        player.draw(screen, camera)

        # HUD kirajzolása
        draw_hud(screen, player)

        # Képernyő frissítése
        pygame.display.flip()


def draw_hud(screen, player):
    """HUD (életerő és pontszám) kirajzolása."""
    font = pygame.font.Font(None, 36)  # Betűtípus és méret
    health_text = font.render(f"Health: {player.health}", True, (255, 255, 255))  # Életerő szöveg
    score_text = font.render(f"Score: {player.score}", True, (255, 255, 255))  # Pontszám szöveg
    screen.blit(health_text, (10, 10))  # Életerő megjelenítése a bal felső sarokban
    screen.blit(score_text, (10, 50))  # Pontszám megjelenítése az életerő alatt


def main_menu(screen):
    """Főmenü megjelenítése."""
    menu_running = True  # A főmenü futását jelző változó
    font = pygame.font.Font(None, 48)  # A betűtípus és méret beállítása
    options = [  # A menü opciói
        LANGUAGES[CURRENT_LANGUAGE]["menu_new_game"],  # Új játék
        LANGUAGES[CURRENT_LANGUAGE]["menu_settings"],  # Beállítások
        LANGUAGES[CURRENT_LANGUAGE]["menu_exit"]  # Kilépés
    ]
    selected_option = 0  # Az alapértelmezett kiválasztott opció indexe

    while menu_running:  # A főmenü ciklusa
        for event in pygame.event.get():  # Események kezelése
            if event.type == pygame.QUIT:  # Ha az ablakot bezárják
                pygame.quit()  # A Pygame bezárása
                exit()  # A program leállítása
            elif event.type == pygame.KEYDOWN:  # Ha egy billentyűt lenyomnak
                if event.key == pygame.K_UP:  # Ha felfele nyíl
                    selected_option = (selected_option - 1) % len(options)  # Az előző opció kiválasztása
                elif event.key == pygame.K_DOWN:  # Ha lefele nyíl
                    selected_option = (selected_option + 1) % len(options)  # A következő opció kiválasztása
                elif event.key == pygame.K_RETURN:  # Ha az ENTER gombot nyomják meg
                    if selected_option == 0:  # Ha az Új játékot választják
                        start_game(screen)  # Játék indítása
                    elif selected_option == 1:  # Ha a Beállításokat választják
                        open_settings(screen)  # Nyelvváltás menü
                    elif selected_option == 2:  # Ha a Kilépést választják
                        pygame.quit()  # A Pygame bezárása
                        exit()  # A program leállítása

        screen.fill(BACKGROUND_COLOR)  # A háttérszín beállítása
        for i, option in enumerate(options):  # A menü opcióinak megjelenítése
            color = WHITE if i == selected_option else (100, 100, 100)  # A kiválasztott opció színe
            text_surface = font.render(option, True, color)  # Az opció szövegének renderelése
            screen.blit(text_surface, (SCREEN_WIDTH // 2 - text_surface.get_width() // 2, 200 + i * 60))  # Szöveg kirajzolása

        pygame.display.flip()  # A képernyő frissítése

def open_settings(screen):
    """Nyelvválasztó menü megjelenítése."""
    menu_running = True  # A nyelvválasztó menü futását jelző változó
    font = pygame.font.Font(None, 48)  # Betűtípus és méret beállítása a nyelvválasztó menühöz
    options = ["English", "Magyar"]  # A választható nyelvek listája
    selected_option = 0  # Az alapértelmezett kiválasztott nyelv indexe

    while menu_running:  # Nyelvválasztó menü ciklusa
        for event in pygame.event.get():  # Események kezelése
            if event.type == pygame.QUIT:  # Ha az ablakot bezárják
                pygame.quit()  # A Pygame bezárása
                exit()  # A program leállítása
            elif event.type == pygame.KEYDOWN:  # Ha egy billentyűt lenyomnak
                if event.key == pygame.K_UP:  # Ha felfelé nyíl gombot nyomják meg
                    selected_option = (selected_option - 1) % len(options)  # Az előző nyelv kiválasztása
                elif event.key == pygame.K_DOWN:  # Ha lefelé nyíl gombot nyomják meg
                    selected_option = (selected_option + 1) % len(options)  # A következő nyelv kiválasztása
                elif event.key == pygame.K_RETURN:  # Ha az ENTER gombot nyomják meg
                    global CURRENT_LANGUAGE  # A globális nyelvváltozó elérése
                    if selected_option == 0:  # Ha az English opciót választják
                        CURRENT_LANGUAGE = "en"  # A nyelv angolra állítása
                    elif selected_option == 1:  # Ha a Magyar opciót választják
                        CURRENT_LANGUAGE = "hu"  # A nyelv magyarra állítása
                    menu_running = False  # Kilépés a nyelvválasztó menüből

        screen.fill(BACKGROUND_COLOR)  # A nyelvválasztó menü háttérszínének beállítása

        for i, option in enumerate(options):  # A nyelvválasztó opcióinak megjelenítése
            color = WHITE if i == selected_option else (100, 100, 100)  # A kiválasztott opció színe
            text_surface = font.render(option, True, color)  # Az opció szövegének renderelése
            screen.blit(text_surface, (SCREEN_WIDTH // 2 - text_surface.get_width() // 2, 200 + i * 60))  # Szöveg kirajzolása

        pygame.display.flip()  # A képernyő frissítése

def pause_menu(screen):
    """Pause menü megjelenítése.""" 
    menu_running = True  # A pause menü futási állapota
    font = pygame.font.Font(None, 48)  # Betűtípus és méret beállítása
    options = [
        LANGUAGES[CURRENT_LANGUAGE]["pause_continue"],  # Folytatás
        LANGUAGES[CURRENT_LANGUAGE]["pause_settings"],  # Beállítások
        LANGUAGES[CURRENT_LANGUAGE]["pause_exit"]  # Kilépés a főmenübe
    ]
    selected_option = 0  # Alapértelmezett kiválasztott opció indexe

    while menu_running:  # Pause menü ciklusa
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Ha az ablakot bezárják
                pygame.quit()  # A Pygame bezárása
                exit()  # A program leállítása
            elif event.type == pygame.KEYDOWN:  # Ha egy billentyűt lenyomnak
                if event.key == pygame.K_UP:  # Felfelé nyíl
                    selected_option = (selected_option - 1) % len(options)  # Előző opció
                elif event.key == pygame.K_DOWN:  # Lefelé nyíl
                    selected_option = (selected_option + 1) % len(options)  # Következő opció
                elif event.key == pygame.K_RETURN:  # Enter lenyomása
                    if selected_option == 0:  # Folytatás opció
                        return "continue"  # Visszatérés a játékba
                    elif selected_option == 1:  # Beállítások opció
                        open_settings(screen)  # Nyelvváltó menü meghívása
                    elif selected_option == 2:  # Kilépés a főmenübe opció
                        return "main_menu"  # Visszatérés a főmenübe

        # Háttérszín beállítása
        screen.fill((50, 50, 50))

        # Menü opciók kirajzolása
        for i, option in enumerate(options):
            color = WHITE if i == selected_option else (100, 100, 100)  # Kiválasztott opció színe
            text_surface = font.render(option, True, color)  # Szöveg renderelése
            screen.blit(text_surface, (SCREEN_WIDTH // 2 - text_surface.get_width() // 2, 200 + i * 60))  # Szöveg kirajzolása

        # Képernyő frissítése
        pygame.display.flip()

# Főmenü inicializálása
main_menu = MainMenu(screen)

# Főmenü ciklusa
menu_running = True  # A főmenü futását jelző változó
running = True  # A játék fő futását jelző változó
main_menu = MainMenu(screen, has_save=True)  # Mentett játék állapota alapján

while menu_running:
    mouse_pos = pygame.mouse.get_pos()
    mouse_pressed = pygame.mouse.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            menu_running = False

        result = main_menu.handle_event(event)
        if result == "new_game":
            start_game(screen)
        elif result == "continue":
            # Ide jön a mentett játék folytatása
            pass
        elif result == "settings":
            # Beállítások menü hívása
            open_settings(screen)  # A nyelvválasztó menü megnyitása
        elif result == "exit":
            menu_running = False

    # A gombok állapotainak frissítése
    main_menu.new_game_button.update_state(mouse_pos, mouse_pressed)
    if main_menu.has_save:
        main_menu.continue_button.update_state(mouse_pos, mouse_pressed)
    main_menu.settings_button.update_state(mouse_pos, mouse_pressed)
    main_menu.exit_button.update_state(mouse_pos, mouse_pressed)

    # A főmenü kirajzolása
    main_menu.draw()
    pygame.display.flip()

pygame.quit()



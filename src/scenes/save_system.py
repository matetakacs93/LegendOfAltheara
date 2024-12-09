import json
import os

SAVE_FILE = "savegame.json"  # Mentési fájl neve

def save_game(data):
    """
    Játék mentése fájlba.
    """
    try:
        with open(SAVE_FILE, "w") as file:
            json.dump(data, file)  # Mentési adatok JSON formátumban írása
        print("Játék mentve.")
    except Exception as e:
        print(f"Mentési hiba: {e}")

def load_game():
    """
    Mentett játék betöltése.
    """
    if not os.path.exists(SAVE_FILE):  # Ellenőrzés, hogy létezik-e mentés
        print("Nincs mentett játék.")
        return None
    try:
        with open(SAVE_FILE, "r") as file:
            data = json.load(file)  # Mentési adatok JSON formátumban olvasása
        print("Játék betöltve.")
        return data
    except Exception as e:
        print(f"Betöltési hiba: {e}")
        return None

def bonfire_interaction(player, save_system, level_name):
    """
    Kezeli a játékos interakcióját a bonfire-rel: visszatölti az életerőt, a manát, és mentést végez.
    """
    # Életerő és mana visszatöltése
    player.health = player.max_health  # Életerő maximálisra állítása
    player.mana = player.max_mana      # Mana maximálisra állítása

    # Játék állapot mentése
    save_system.save_game(level_name, player)  # Mentés a jelenlegi szint és játékos állapottal

    print("Bonfire: Életerő és mana visszatöltve, játék mentve!")  # Konzolüzenet

def save_at_bonfire(player, current_level):
    """
    Mentési rendszer a bonfire-nél.
    """
    save_data = {
        "player": {
            "position": (player.rect.x, player.rect.y),
            "health": player.health,
            "mana": player.mana,
            "level": player.level,
            "xp": player.xp,
        },
        "current_level": current_level,
    }

    with open("save_data.json", "w") as save_file:
        json.dump(save_data, save_file)
        print("Játék mentve a bonfire-nél.")

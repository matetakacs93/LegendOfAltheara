import json
import pygame

def load_level_data(file_path):
    """Betölti a pálya adatait a JSON fájlból."""
    try:
        with open(file_path, "r") as file:
            data = json.load(file)
        print("JSON fájl sikeresen betöltve!")
        return data
    except json.JSONDecodeError as e:
        print(f"JSON hiba: {e}")
        return None
    except FileNotFoundError:
        print(f"A fájl nem található: {file_path}")
        return None

def load_tileset(uid):
    """Betölti a tileset képeket a JSON alapján."""
    tilesets = {
        1: "assets/tilesets/level1/forest2.png",  # Hegyi csempék
        3: "assets/tilesets/level1/forestdekor16x16.png"  # Vizes csempék
    }
    if uid not in tilesets:
        print(f"Hiba: Az uid {uid} nem található a tilesets dictionary-ben.")
        return None

    tileset_image = pygame.image.load(tilesets[uid]).convert_alpha()
    tiles = {}

    tile_size = 64  # Egy csempe mérete
    for y in range(tileset_image.get_height() // tile_size):
        for x in range(tileset_image.get_width() // tile_size):
            tile_id = y * (tileset_image.get_width() // tile_size) + x
            rect = pygame.Rect(x * tile_size, y * tile_size, tile_size, tile_size)
            tiles[tile_id] = tileset_image.subsurface(rect).copy()
    return tiles

def draw_level(data, screen, camera):
    """Kirajzolja a pályát a JSON fájl alapján."""
    # Ellenőrzés, hogy van-e 'layers' kulcs
    if 'layers' not in data:
        print("A JSON fájl nem tartalmaz 'layers' kulcsot.")
        return

    for layer in data['layers']:
        if layer['__type'] == 'Tiles':  # Csak a csempéket rajzoljuk ki
            tileset = load_tileset(layer['__tilesetDefUid'])  # Tileset betöltése
            if not tileset:
                continue

            for tile in layer['gridTiles']:
                x = tile['px'][0]  # X koordináta
                y = tile['px'][1]  # Y koordináta
                tile_id = tile['t']  # Tile azonosító

                # Kirajzolás a kamera pozíciójának figyelembevételével
                screen.blit(tileset[tile_id], camera.apply_rect(pygame.Rect(x, y, 64, 64)))


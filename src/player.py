import pygame
import os
from settings import SCREEN_WIDTH

class Player:
    def __init__(self, x, y):
        self.animations = {"idle": [], "run": [], "jump": []}  # Animációk betöltése
        self.current_animation = "idle"  # Alapértelmezett animáció
        self.current_frame = 0  # Aktuális frame index
        self.frame_delay = 100  # Animáció frame-váltási késleltetés
        self.last_update = pygame.time.get_ticks()  # Utolsó frissítés időpontja

        self.rect = pygame.Rect(x, y, 256, 256)  # Játékos mérete és pozíciója
        self.velocity_x = 0  # Vízszintes sebesség
        self.velocity_y = 0  # Függőleges sebesség
        self.gravity = 1500  # Gravitáció ereje
        self.jump_strength = -700  # Ugrás ereje
        self.on_ground = False  # Földön áll-e a játékos

        self.health = 100  # Aktuális életerő
        self.max_health = 100  # Maximális életerő
        self.xp = 0
        self.xp_needed = 100
        self.level = 1
        self.attack = 10  # Támadó erő
        self.defense = 5  # Védekező erő

        self.facing_right = True  # Játékos iránya

        self.load_animations()  # Animációk betöltése

    def load_animations(self):
        """Animációk betöltése különböző állapotokhoz."""
        animation_types = ["idle", "run", "jump"]
        for anim_type in animation_types:
            path = f"assets/sprites/player/{anim_type}"
            self.animations[anim_type] = []
            for file_name in sorted(os.listdir(path)):
                if file_name.endswith(".png"):
                    frame = pygame.image.load(os.path.join(path, file_name)).convert_alpha()
                    frame = pygame.transform.scale(frame, (256, 256))
                    self.animations[anim_type].append(frame)

    def animate(self):
        """Aktuális animáció kezelése."""
        if not self.animations[self.current_animation]:
            return pygame.Surface((256, 256))

        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_delay:
            self.current_frame = (self.current_frame + 1) % len(self.animations[self.current_animation])
            self.last_update = now
        return self.animations[self.current_animation][self.current_frame]

    def collect_loot(self, loots):
        """Lootok felszedése."""
        for loot in loots:
            if self.rect.colliderect(loot.rect):
                if loot.loot_type == "health":
                    self.health = min(self.health + 10, self.max_health)  # Életerő növelése max. értékig
                elif loot.loot_type == "coin":
                    self.score += 10  # Pontszám növelése
                loot.kill()  # Loot eltávolítása

    def gain_xp(self, amount):
        """XP gyűjtése."""
        self.xp += amount
        if self.xp >= self.xp_needed:
            self.level_up()

    def level_up(self):
        """Szintlépés logikája."""
        self.level += 1
        self.xp = 0  # XP visszaállítása
        self.xp_needed += 50  # Következő szinthez több XP szükséges
        self.max_health += 20  # Életerő növelése
        self.health = self.max_health  # Teljes életerő visszaállítása

    def update(self, keys, delta_time, platforms, loots):
        """Játékos frissítése."""
        speed = 400  # Mozgási sebesség

        # Mozgás kezelése
        if keys[pygame.K_LEFT]:
            self.velocity_x = -speed
            self.current_animation = "run"
            self.facing_right = False
        elif keys[pygame.K_RIGHT]:
            self.velocity_x = speed
            self.current_animation = "run"
            self.facing_right = True
        else:
            self.velocity_x = 0
            if self.on_ground:
                self.current_animation = "idle"

        # Ugrás
        if keys[pygame.K_SPACE] and self.on_ground:
            self.velocity_y = self.jump_strength
            self.current_animation = "jump"

        # Gravitáció és mozgás alkalmazása
        self.velocity_y += self.gravity * delta_time
        self.rect.y += self.velocity_y * delta_time
        self.rect.x += self.velocity_x * delta_time

        self.on_ground = False
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.velocity_y > 0:
                    self.rect.bottom = platform.rect.top
                    self.velocity_y = 0
                    self.on_ground = True

        # Játékos képernyőn tartása
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH

        # Lootok felszedése
        self.collect_loot(loots)

    def draw(self, screen, camera):
        """Játékos kirajzolása."""
        frame = self.animate()  # Aktuális frame lekérése
        if not self.facing_right:
            frame = pygame.transform.flip(frame, True, False)  # Tükrözés bal irány esetén
        screen.blit(frame, camera.apply(self))  # Frame megjelenítése a kamerán belül

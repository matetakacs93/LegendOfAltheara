import pygame
import os
from settings import SCREEN_WIDTH, SCREEN_HEIGHT

class Player:
    def __init__(self, x, y):
        self.animations = {"idle": [], "run": [], "jump": []}  # Animációk tárolása
        self.current_animation = "idle"  # Aktuális animáció
        self.current_frame = 0  # Aktuális animációs keret
        self.frame_delay = 100  # Animációs sebesség
        self.last_update = pygame.time.get_ticks()  # Utolsó frissítés ideje

        self.rect = pygame.Rect(x, y, 256, 256)  # Játékos pozíció és méret
        self.velocity_x = 0  # Vízszintes sebesség
        self.velocity_y = 0  # Függőleges sebesség
        self.gravity = 1500  # Gravitáció
        self.jump_strength = -700  # Ugrás erőssége
        self.on_ground = False  # Földön van-e a játékos
        self.health = 100  # Életerő
        self.max_health = 100  # Maximális életerő
        self.coins = 0  # Összegyűjtött érmék
        self.xp = 0  # Játékos jelenlegi tapasztalati pontjai
        self.xp_needed = 100  # Következő szinthez szükséges XP
        self.level = 1  # Játékos szintje

        self.attack_cooldown = 0  # Támadás lehűlési idő
        self.facing_right = True  # Játékos nézési iránya

        self.load_animations()  # Animációk betöltése

    def load_animations(self):
        animation_types = ["idle", "run", "jump", "attack"]  # Az animációk típusai
        for anim_type in animation_types:
            path = f"assets/sprites/player/{anim_type}"  # Útvonal az adott animációhoz
            if not os.path.exists(path):
                print(f"{anim_type} animáció betöltve: {len(self.animations[anim_type])} frame")
            continue
        self.animations[anim_type] = []  # Inicializáljuk az animációs listát
        for file_name in sorted(os.listdir(path)):
            if file_name.endswith(".png"):
                frame = pygame.image.load(os.path.join(path, file_name)).convert_alpha()
                frame = pygame.transform.scale(frame, (256, 256))  # Méretezés
                self.animations[anim_type].append(frame)

        if not self.animations[anim_type]:  # Ellenőrizzük, hogy betöltöttek-e frame-eket
            print(f"HIBA: Nincs betöltött frame az animációhoz: {anim_type}")

          
    def animate(self):
        """Az aktuális animáció frissítése és visszatérési frame."""
        if not self.animations[self.current_animation]:  # Ha nincs betöltve animáció
            print(f"HIBA: Nincs betöltött frame az animációhoz: {self.current_animation}")  # Hibajelzés
            return pygame.Surface((256, 256))  # Egy üres fekete kép visszaadása
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_delay:
            self.current_frame = (self.current_frame + 1) % len(self.animations[self.current_animation])
            self.last_update = now
        return self.animations[self.current_animation][self.current_frame]


    def gain_xp(self, amount):
        """XP növelése."""
        self.xp += amount
        if self.xp >= self.xp_needed:
            self.level_up()

    def level_up(self):
        """Szintlépés logikája."""
        self.level += 1
        self.xp -= self.xp_needed
        self.xp_needed += 50  # Következő szinthez több XP kell
        self.max_health += 10  # Maximális életerő növelése
        self.health = self.max_health  # Életerő feltöltése szintlépéskor

    def update(self, keys, delta_time, platforms, loots, enemies):
        speed = 400  # Játékos sebessége

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

        if keys[pygame.K_SPACE] and self.on_ground:
            self.velocity_y = self.jump_strength
            self.current_animation = "jump"

        if keys[pygame.K_q]:
            self.attack()
            if self.is_attacking:
                if self.current_animation != "attack":
                    self.is_attacking = False  # Animáció vége
        else:
            now = pygame.time.get_ticks()
            if now - self.last_update > self.frame_delay:
                self.current_frame += 1
                if self.current_frame >= len(self.animations["attack"]):
                    self.is_attacking = False  # Támadás vége
                    self.current_animation = "idle"
                self.last_update = now
            else:
                self.current_animation = "idle"  # Alapállapot
        

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

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH

        self.collect_loot(loots)  # Loot összegyűjtése
        self.check_enemies_collision(enemies)  # Ellenségekkel való interakció

        if self.attack_cooldown > 0:
            self.attack_cooldown -= delta_time

    def attack(self):
        """Támadás logikája."""
        if self.attack_cooldown <= 0:
            self.is_attacking = True
            self.current_animation = "attack"
            self.current_frame = 0  # Animáció elejére ugrik
            self.attack_cooldown = 1.0  # 1 másodperces lehűlési idő

    def collect_loot(self, loots):
        """Lootok összegyűjtése."""
        for loot in loots:
            if self.rect.colliderect(loot.rect):
                if loot.loot_type == "health":
                    self.health = min(self.health + 20, self.max_health)
                elif loot.loot_type == "coin":
                    self.coins += 1
                loots.remove(loot)

    def check_enemies_collision(self, enemies):
        """Ellenségekkel való interakció."""
        for enemy in enemies:
            if self.rect.colliderect(enemy.rect):
                self.health -= 10  # Csökkenti az életerőt
                if self.health <= 0:
                    print("Game Over!")  # Játék vége logika ide

    def draw(self, screen, camera):
        frame = self.animate()
        if not self.facing_right:
            frame = pygame.transform.flip(frame, True, False)
        screen.blit(frame, camera.apply(self))  # Játékos megjelenítése




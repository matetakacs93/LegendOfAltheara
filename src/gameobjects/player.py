import pygame  # A pygame modul importálása, amely a játékfejlesztéshez szükséges.
import os  # Az operációs rendszerrel való munkához szükséges modul.
from settings import SCREEN_WIDTH, SCREEN_HEIGHT  # Beállítások importálása a képernyő méretéhez.

class Player:  # A játékos osztály definiálása.
    def __init__(self, x, y):  # Az osztály inicializálási metódusa.
        self.animations = {"idle": [], "run": [], "jump": [], "attack": []}  # Az animációkat tartalmazó szótár.
        self.current_animation = "idle"  # Az aktuális animáció kezdőállapota.
        self.current_frame = 0  # Az animáció aktuális képkockája.
        self.frame_delay = 100  # Az animáció képkockáinak váltása közötti idő milliszekundumban.
        self.last_update = pygame.time.get_ticks()  # Az utolsó frissítés időbélyege.
        self.animation_delays = {"idle": 100, "run": 100, "jump": 150, "attack": 300}  # Animáció késleltetések.

        self.rect = pygame.Rect(x, y, 256, 256)  # A játékos téglalap alakú kerete.
        self.velocity_x = 0  # Vízszintes sebesség.
        self.velocity_y = 0  # Függőleges sebesség.
        self.gravity = 1500  # Gravitáció mértéke.
        self.jump_strength = -700  # Ugrási erő.
        self.on_ground = False  # Logikai érték: földön van-e a játékos.
        self.score = 0  # Pontszám kezdőértéke.
        self.health = 100  # Életerő kezdőértéke.
        self.max_health = 100  # Maximális életerő.
        self.mana = 50  # Mana kezdőértéke.
        self.max_mana = 100  # Maximális mana.
        self.coins = 0  # Érmék száma.
        self.xp = 0  # Tapasztalati pontok száma.
        self.xp_to_level = 100  # Szintlépéshez szükséges XP.
        self.level = 1  # Játékos szintje.
        self.posture = 100  # Posture érték.
        self.max_posture = 100
        self.parry_window = 300  # Parry időablak milliszekundumban.
        self.last_parry_time = 0

        self.attack_cooldown = 300  # Támadások közötti várakozási idő.
        self.last_attack_time = 0  # Utolsó támadás időbélyege.
        self.is_attacking = False  # Logikai érték: támadás folyamatban van-e.
        self.facing_right = True  # Logikai érték: jobbra néz-e a játékos.

        self.load_animations()  # Animációk betöltése.

    def load_animations(self):  # Animációk betöltése.
        animation_types = ["idle", "run", "jump", "attack"]
        for anim_type in animation_types:
            path = f"assets/sprites/player/{anim_type}"
            self.animations[anim_type] = []
            if not os.path.exists(path):
                print(f"HIBA: Animációs mappa nem létezik: {path}")
                continue
            for file_name in sorted(os.listdir(path)):
                if file_name.endswith(".png"):
                    try:
                        frame = pygame.image.load(os.path.join(path, file_name)).convert_alpha()
                        frame = pygame.transform.scale(frame, (256, 256))
                        self.animations[anim_type].append(frame)
                    except Exception as e:
                        print(f"HIBA: Nem sikerült betölteni a fájlt {file_name}. Hiba: {e}")

    def animate(self):
        if self.current_animation not in self.animations or not self.animations[self.current_animation]:
            return pygame.Surface((256, 256))  # Üres képet ad vissza.

        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_delay:
            self.current_frame = (self.current_frame + 1) % len(self.animations[self.current_animation])
            self.last_update = now

        return self.animations[self.current_animation][self.current_frame]

    def update(self, keys, delta_time, platforms, loots, enemies):
        speed = 400
        self.animate()

        if self.is_attacking:
            if self.current_animation != "attack":
                self.current_animation = "attack"
            if self.current_frame >= len(self.animations["attack"]) - 1:
                self.is_attacking = False
                self.current_animation = "idle" if self.velocity_x == 0 else "run"
            return

        if keys[pygame.K_q] and not self.is_attacking and self.on_ground:
            now = pygame.time.get_ticks()
            if now - self.last_attack_time > self.attack_cooldown:
                self.is_attacking = True
                self.last_attack_time = now
                self.current_animation = "attack"
                self.current_frame = 0
            return

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
            if not self.is_attacking:
                self.current_animation = "jump"

        self.velocity_y += self.gravity * delta_time
        self.rect.y += self.velocity_y * delta_time
        self.rect.x += self.velocity_x * delta_time

        for platform in platforms:
            if self.rect.colliderect(platform.rect) and self.velocity_y > 0:
                self.rect.bottom = platform.rect.top
                self.velocity_y = 0
                self.on_ground = True
                break
        else:
            self.on_ground = False

    def draw(self, screen, camera):
        frame = self.animate()
        if not self.facing_right:
            frame = pygame.transform.flip(frame, True, False)
        screen.blit(frame, camera.apply(self))

    def attack(self):
        if not self.on_ground:
            print("Nem támadhatsz a levegőben!")
            return

        now = pygame.time.get_ticks()
        if now - self.last_attack_time > self.attack_cooldown:
            self.is_attacking = True
            self.last_attack_time = now
            self.current_animation = "attack"
            self.current_frame = 0

    def is_on_ground(self):
        return self.on_ground

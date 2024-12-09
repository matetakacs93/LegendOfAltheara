import pygame  # A pygame modul importálása, amely a játékfejlesztéshez szükséges.
import os  # Az operációs rendszerrel való munkához szükséges modul.
from settings import SCREEN_WIDTH, SCREEN_HEIGHT  # Beállítások importálása a képernyő méretéhez.

class Player:  # A játékos osztály definiálása.
    def __init__(self, x, y):  # Az osztály inicializálási metódusa, amely meghatározza a játékos kezdőállapotát.
        self.animations = {"idle": [], "run": [], "jump": [], "attack": []}  # Az animációkat tartalmazó szótár.
        self.current_animation = "idle"  # Az aktuális animáció kezdőállapota.
        self.current_frame = 0  # Az animáció aktuális képkockája.
        self.frame_delay = 100  # Az animáció képkockáinak váltása közötti idő milliszekundumban.
        self.last_update = pygame.time.get_ticks()  # Az utolsó frissítés időbélyege.
        self.animation_delays = {"idle": 100, "run": 100, "jump": 150, "attack": 300}  # Az animációk késleltetéseinek beállítása.

        self.rect = pygame.Rect(x, y, 256, 256)  # A játékos téglalap alakú kerete, amelyet az x és y koordináták határoznak meg.
        self.velocity_x = 0  # A vízszintes sebesség kezdőértéke.
        self.velocity_y = 0  # A függőleges sebesség kezdőértéke.
        self.gravity = 1500  # A gravitáció mértéke, amely lefelé húzza a játékost.
        self.jump_strength = -700  # Az ugrási erő, amely felfelé mozgatja a játékost.
        self.on_ground = False  # Logikai érték, amely azt jelzi, hogy a játékos a földön van-e.
        self.health = 100  # A játékos kezdő életereje.
        self.max_health = 100  # A játékos maximális életereje.
        self.coins = 0  # Az összegyűjtött érmék száma.
        self.xp = 0  # A megszerzett tapasztalati pontok száma.
        self.xp_needed = 100  # A szintlépéshez szükséges tapasztalati pontok száma.
        self.level = 1  # A játékos szintje.

        self.attack_cooldown = 300  # A támadások közötti várakozási idő milliszekundumban.
        self.last_attack_time = 0  # Az utolsó támadás időbélyege.
        self.is_attacking = False  # Logikai érték, amely azt jelzi, hogy a játékos éppen támad-e.
        self.facing_right = True  # Logikai érték, amely azt jelzi, hogy a játékos jobbra néz-e.

        self.load_animations()  # Az animációk betöltése.

    def load_animations(self):  # Metódus az animációk betöltésére.
        animation_types = ["idle", "run", "jump", "attack"]  # Az animáció típusai.
        for anim_type in animation_types:  # Minden animáció típusra.
            path = f"assets/sprites/player/{anim_type}"  # Az animáció fájljainak útvonala.
            self.animations[anim_type] = []  # Az aktuális animáció üres listával való inicializálása.
            if not os.path.exists(path):  # Ellenőrzés, hogy létezik-e az útvonal.
                print(f"HIBA: Az animációs mappa nem létezik: {path}")  # Hibaüzenet, ha nem létezik.
                continue  # Lépjen a következő animációra.
            for file_name in sorted(os.listdir(path)):  # Az animáció fájljainak átnézése.
                if file_name.endswith(".png"):  # Csak a PNG fájlok betöltése.
                    try:
                        frame = pygame.image.load(os.path.join(path, file_name)).convert_alpha()  # A kép betöltése.
                        frame = pygame.transform.scale(frame, (256, 256))  # A kép átméretezése.
                        self.animations[anim_type].append(frame)  # A kép hozzáadása az animáció listájához.
                    except Exception as e:  # Hiba esetén.
                        print(f"HIBA: Nem sikerült betölteni a fájlt {file_name}. Hiba: {e}")  # Hibaüzenet megjelenítése.
            if not self.animations[anim_type]:  # Ha nincs betöltött animáció.
                print(f"HIBA: Az {anim_type} animáció üres!")  # Hibaüzenet megjelenítése.
            else:
                print(f"{anim_type} animáció betöltött frame-ek száma: {len(self.animations[anim_type])}")  # Sikeres betöltés üzenete.

    def animate(self):  # Az animáció frissítése.
        if self.current_animation not in self.animations or not self.animations[self.current_animation]:  # Ha az animáció nem található vagy üres.
            print(f"HIBA: Nincs frame az animációhoz: {self.current_animation}")  # Hibaüzenet.
            return pygame.Surface((256, 256))  # Üres képet ad vissza.

        now = pygame.time.get_ticks()  # Az aktuális idő.
        if now - self.last_update > self.frame_delay:  # Ha elég idő telt el a következő képkockához.
            self.current_frame = (self.current_frame + 1) % len(self.animations[self.current_animation])  # Következő képkockára lép.
            self.last_update = now  # Az utolsó frissítés idejének frissítése.

        return self.animations[self.current_animation][self.current_frame]  # Az aktuális képkockát adja vissza.

    def update(self, keys, delta_time, platforms, loots, enemies):  # A játékos állapotának frissítése.
        speed = 400  # A játékos mozgási sebessége.
        self.animate()  # Animáció frissítése.

        if self.is_attacking:  # Ha a játékos támad.
            if self.current_animation != "attack":  # Ha az animáció nem a támadás.
                self.current_animation = "attack"  # Állítsa be a támadási animációt.
            if self.current_frame >= len(self.animations["attack"]) - 1:  # Ha a támadási animáció véget ért.
                self.is_attacking = False  # Fejezze be a támadást.
                self.current_animation = "idle" if self.velocity_x == 0 else "run"  # Állítsa be az alapértelmezett animációt.
            return  # Lépjen ki.

        if keys[pygame.K_q] and not self.is_attacking:  # Ha a támadási gombot lenyomják, és nem támad.
            now = pygame.time.get_ticks()  # Az aktuális idő.
            if now - self.last_attack_time > self.attack_cooldown:  # Ha letelt a támadási cooldown.
                self.is_attacking = True  # Indítsa el a támadást.
                self.last_attack_time = now  # Frissítse az utolsó támadás időbélyegét.
                self.current_animation = "attack"  # Állítsa be a támadási animációt.
                self.current_frame = 0  # Az animáció elejére áll.
            return  # Lépjen ki.

        if keys[pygame.K_LEFT]:  # Ha a bal nyilat lenyomják.
            self.velocity_x = -speed  # Mozgás balra.
            self.current_animation = "run"  # Futtatási animáció.
            self.facing_right = False  # A játékos balra néz.
        elif keys[pygame.K_RIGHT]:  # Ha a jobb nyilat lenyomják.
            self.velocity_x = speed  # Mozgás jobbra.
            self.current_animation = "run"  # Futtatási animáció.
            self.facing_right = True  # A játékos jobbra néz.
        else:  # Ha nem nyomnak mozgási gombot.
            self.velocity_x = 0  # A játékos megáll.
            if self.on_ground:  # Ha a földön van.
                self.current_animation = "idle"  # Álló animáció.

        if keys[pygame.K_SPACE] and self.on_ground:  # Ha az ugrási gombot lenyomják, és a földön van.
            self.velocity_y = self.jump_strength  # Ugrás.
            if not self.is_attacking:  # Ha nem támad.
                self.current_animation = "jump"  # Ugrási animáció.

        self.velocity_y += self.gravity * delta_time  # A gravitáció hatása a sebességre.
        self.rect.y += self.velocity_y * delta_time  # Függőleges mozgás frissítése.
        self.rect.x += self.velocity_x * delta_time  # Vízszintes mozgás frissítése.

        for platform in platforms:  # Minden platform esetén.
            if self.rect.colliderect(platform.rect) and self.velocity_y > 0:  # Ha a játékos ütközik egy platformmal fentről.
                self.rect.bottom = platform.rect.top  # Állítsa be a pozícióját a platform tetejére.
                self.velocity_y = 0  # Állítsa le a függőleges mozgást.
                self.on_ground = True  # Állítsa be, hogy a játékos a földön van.
                break  # Lépjen ki a ciklusból.
        else:  # Ha nincs ütközés.
            self.on_ground = False  # A játékos nincs a földön.

    def draw(self, screen, camera):  # A játékos megjelenítése a képernyőn.
        frame = self.animate()  # Az aktuális animáció képkockája.
        if not self.facing_right:  # Ha a játékos balra néz.
            frame = pygame.transform.flip(frame, True, False)  # Fordítsa meg a képet.
        screen.blit(frame, camera.apply(self))  # Rajzolja ki a játékost a képernyőre.




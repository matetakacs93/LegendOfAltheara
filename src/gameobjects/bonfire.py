import pygame

class Bonfire(pygame.sprite.Sprite):
    def __init__(self, x, y, image_paths):
        super().__init__()
        self.images = [pygame.image.load(path).convert_alpha() for path in image_paths]
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect(topleft=(x, y))
        self.animation_speed = 0.1
        self.current_time = 0

    def update(self, delta_time):
        self.current_time += delta_time
        if self.current_time >= self.animation_speed:
            self.current_time = 0
            self.index = (self.index + 1) % len(self.images)
            self.image = self.images[self.index]




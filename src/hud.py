import pygame

class HUD:
    def __init__(self, screen, player):
        self.screen = screen
        self.player = player
        self.font = pygame.font.Font(None, 36)

    def draw(self):
        # Életerő csík
        pygame.draw.rect(self.screen, (255, 0, 0), (20, 20, 200, 20))  # Háttér piros
        pygame.draw.rect(self.screen, (0, 255, 0), (20, 20, 200 * (self.player.health / self.player.max_health), 20))  # Zöld csík

        # Érmék számláló
        coin_text = self.font.render(f"Coins: {self.player.coins}", True, (255, 255, 255))
        self.screen.blit(coin_text, (20, 50))

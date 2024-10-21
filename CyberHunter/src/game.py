import pygame
import sys

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, speed, strength):
        super().__init__()
        self.image = pygame.Surface((5, 10))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = speed
        self.strength = strength

    def update(self):
        self.rect.y -= self.speed
        if self.rect.bottom < 0:
            self.kill()

def game_loop(screen, road_image, selected_character_data, all_sprites, enemies, clock, font, SCREEN_WIDTH, SCREEN_HEIGHT, score):
    player_color = selected_character_data["color"]
    player_speed = selected_character_data["speed"]
    player_image = pygame.image.load(selected_character_data["image"])
    player_image = pygame.transform.scale(player_image, (50, 100))
    player_rect = player_image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100))

    road_y = 0  # Initial position of the road
    score_timer = pygame.time.get_ticks()  # Timer to track score increment
    bullet_timer = pygame.time.get_ticks()  # Timer to control firing rate
    bullet_speed = 10
    bullet_strength = 1
    bullets = pygame.sprite.Group()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and player_rect.left > 0:
            player_rect.x -= player_speed
        if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and player_rect.right < SCREEN_WIDTH:
            player_rect.x += player_speed
        if (keys[pygame.K_UP] or keys[pygame.K_w]) and player_rect.top > 0:
            player_rect.y -= player_speed
        if (keys[pygame.K_DOWN] or keys[pygame.K_s]) and player_rect.bottom < SCREEN_HEIGHT:
            player_rect.y += player_speed

        # Fire bullets automatically when space is held down
        if keys[pygame.K_SPACE]:
            current_time = pygame.time.get_ticks()
            if current_time - bullet_timer >= 200:  # Fire rate: one bullet every 200 milliseconds
                bullet = Bullet(player_rect.centerx, player_rect.top, bullet_speed, bullet_strength)
                bullets.add(bullet)
                all_sprites.add(bullet)
                bullet_timer = current_time

        # Move the road
        road_y += player_speed
        if road_y >= SCREEN_HEIGHT:
            road_y = 0

        # Update score every second
        current_time = pygame.time.get_ticks()
        if current_time - score_timer >= 1000:  # 1000 milliseconds = 1 second
            score += 100
            score_timer = current_time

        # Update bullets
        bullets.update()

        # Draw the road twice to create a continuous scrolling effect
        screen.blit(road_image, (0, road_y - SCREEN_HEIGHT))
        screen.blit(road_image, (0, road_y))

        # Draw the player car
        screen.blit(player_image, player_rect)

        # Draw the score at the top middle of the screen
        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, 30))
        screen.blit(score_text, score_rect)

        # Draw bullets
        bullets.draw(screen)

        pygame.display.flip()
        clock.tick(60)
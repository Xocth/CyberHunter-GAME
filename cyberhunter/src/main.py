# config.py
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

characters = [
    {"name": "Daniel", "color": (0, 255, 0), "speed": 6, "strength": 7, "agility": 7, "image": "cyberhunter/images/cars/daniel_car.png"},  # Green car
    {"name": "Mo", "color": (128, 0, 128), "speed": 8, "strength": 6, "agility": 6, "image": "cyberhunter/images/cars/mo_car.png"},   # Purple car
    {"name": "Rene", "color": (0, 0, 255), "speed": 6, "strength": 8, "agility": 6, "image": "cyberhunter/images/cars/rene_car.png"},   # Blue car
    {"name": "Owen", "color": (255, 105, 180), "speed": 7, "strength": 7, "agility": 6, "image": "cyberhunter/images/cars/owen_car.png"},  # Hot pink car
]

# enemy.py
import pygame
import sys

# Initialize pygame
pygame.init()

# Initialize the mixer
pygame.mixer.init()

# Load the explosion sound
explosion_sound = pygame.mixer.Sound("cyberhunter/audio/8bit_explosion.mp3")

# Load the player hurt sound
player_hurt_sound = pygame.mixer.Sound("cyberhunter/audio/playerhurt.mp3")

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, speed):
        super().__init__()
        self.image = pygame.image.load("cyberhunter/images/cars/enemy.png")
        self.image = pygame.transform.scale(self.image, (100, 150))
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = speed
        self.health = 20

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > pygame.display.get_surface().get_height():
            self.kill()

    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.kill()
            explosion_sound.play()  # Play the explosion sound
            return 20  # Points awarded for destroying the enemy
        return 0

# menu.py
import pygame
import sys

def draw_text(surface, text, font, color, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

def draw_stat_bar(surface, x, y, width, height, value, max_value, color):
    pygame.draw.rect(surface, (255, 255, 255), (x, y, width, height), 1)  # Border
    inner_width = (value / max_value) * (width - 2)
    pygame.draw.rect(surface, color, (x + 1, y + 1, inner_width, height - 2))

def menu_loop(screen, font, selected_character):
    difficulty = "Normal"
    difficulties = ["Easy", "Normal", "Hard"]
    selected_difficulty = 1  # Default to "Normal"

    # Load menu background image
    menu_background = pygame.image.load("cyberhunter/images/menubkg.png")
    menu_background = pygame.transform.scale(menu_background, (SCREEN_WIDTH, SCREEN_HEIGHT))

    # Load and play menu music
    pygame.mixer.music.load("cyberhunter/audio/menumsc.ogg")
    pygame.mixer.music.play(-1)  # Loop the music indefinitely

    while True:
        screen.fill((0, 0, 0))
        
        # Draw the menu background image
        screen.blit(menu_background, (0, 0))
        
        # Options Positioning
        center_x = SCREEN_WIDTH // 2.25 
        bottom_y = SCREEN_HEIGHT - 250

        # Display "Character :" label
        draw_text(screen, "Character :", font, (255, 255, 255), center_x - 150, bottom_y)
        
        # Display selected character
        character = characters[selected_character]
        color = character["color"]
        draw_text(screen, character["name"], font, color, center_x + 100, bottom_y)

        # Display character stats
        max_stat_value = 10  # Assuming max value for any stat is 10
        stat_bar_width = 200
        stat_bar_height = 20
        stat_y_offset = 30

        draw_stat_bar(screen, center_x - 150, bottom_y + stat_y_offset, stat_bar_width, stat_bar_height, character["speed"], max_stat_value, (0, 0, 255))
        draw_text(screen, "Speed", font, (255, 255, 255), center_x - 150 + stat_bar_width + 10, bottom_y + stat_y_offset)

        draw_stat_bar(screen, center_x - 150, bottom_y + stat_y_offset * 2, stat_bar_width, stat_bar_height, character["strength"], max_stat_value, (0, 255, 0))
        draw_text(screen, "Strength", font, (255, 255, 255), center_x - 150 + stat_bar_width + 10, bottom_y + stat_y_offset * 2)

        draw_stat_bar(screen, center_x - 150, bottom_y + stat_y_offset * 3, stat_bar_width, stat_bar_height, character["agility"], max_stat_value, (255, 0, 0))
        draw_text(screen, "Agility", font, (255, 255, 255), center_x - 150 + stat_bar_width + 10, bottom_y + stat_y_offset * 3)

        # Display difficulty setting
        draw_text(screen, "Question Difficulty: " + difficulty, font, (255, 255, 255), center_x - 150, bottom_y + stat_y_offset * 4 + 30)
        draw_text(screen, "Press Enter to Start", font, (255, 255, 255), center_x - 150, bottom_y + stat_y_offset * 4 + 90)
        draw_text(screen, "Press Esc to Exit", font, (255, 255, 255), center_x - 150, bottom_y + stat_y_offset * 4 + 150)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    selected_character = (selected_character - 1) % len(characters)
                elif event.key == pygame.K_RIGHT:
                    selected_character = (selected_character + 1) % len(characters)
                elif event.key == pygame.K_a:
                    selected_difficulty = (selected_difficulty - 1) % len(difficulties)
                    difficulty = difficulties[selected_difficulty]
                elif event.key == pygame.K_d:
                    selected_difficulty = (selected_difficulty + 1) % len(difficulties)
                    difficulty = difficulties[selected_difficulty]
                elif event.key == pygame.K_RETURN:
                    pygame.mixer.music.stop()  # Stop the music when starting the game
                    return selected_character, difficulty
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

# game.py
import pygame
import sys
import random
from datetime import datetime
import json
import os

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

class Player(pygame.sprite.Sprite):
    def __init__(self, image, x, y, speed):
        super().__init__()
        self.image = pygame.transform.scale(image, (100, 150))
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = speed
        self.health = 3

    def update(self, keys):
        if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and self.rect.left > 0:
            self.rect.x -= self.speed
        if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and self.rect.right < SCREEN_WIDTH:
            self.rect.x += self.speed
        if (keys[pygame.K_UP] or keys[pygame.K_w]) and self.rect.top > 0:
            self.rect.y -= self.speed
        if (keys[pygame.K_DOWN] or keys[pygame.K_s]) and self.rect.bottom < SCREEN_HEIGHT:
            self.rect.y += self.speed

    def take_damage(self, damage):
        self.health -= damage
        print(f"Player took damage: {damage}, health left: {self.health}")  # Debug print
        
        if self.health <= 0:
            self.kill()

def game_over_screen(screen, font, score, character_name):
    screen.fill((0, 0, 0))
    game_over_text = font.render("Game Over", True, (255, 0, 0))
    score_text = font.render(f"Final Score: {score}", True, (255, 255, 255))
    enter_name_text = font.render("Enter your name:", True, (255, 255, 255))
    continue_text = font.render("Press Enter to Continue", True, (255, 255, 255))

    game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100))
    score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
    enter_name_rect = enter_name_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    continue_rect = continue_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100))

    name = ""
    input_active = True

    while input_active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    input_active = False
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                elif len(name) < 15:
                    name += event.unicode

        screen.fill((0, 0, 0))
        screen.blit(game_over_text, game_over_rect)
        screen.blit(score_text, score_rect)
        screen.blit(enter_name_text, enter_name_rect)
        name_text = font.render(name, True, (255, 255, 255))
        name_rect = name_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
        screen.blit(name_text, name_rect)
        screen.blit(continue_text, continue_rect)
        pygame.display.flip()

    # Save the name, score, current time, and character name to a file
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("scores.txt", "a") as file:
        file.write(f"Name: {name}, Score: {score}, Character: {character_name}, Time: {current_time}\n")

    # Print the time in the terminal
    print(f"Game Over at: {current_time}")

    return name

def next_level_screen(screen, font, difficulty):
    screen.fill((0, 0, 0))
    message_text = font.render("You successfully beat this stage!", True, (255, 255, 255))
    instruction_text = font.render("Answer these questions to proceed to the next level", True, (255, 255, 255))
    difficulty_text = font.render(f"Difficulty: {difficulty}", True, (255, 255, 255))
    continue_text = font.render("Press Enter to Continue", True, (255, 255, 255))

    message_rect = message_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100))
    instruction_rect = instruction_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
    difficulty_rect = difficulty_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    continue_rect = continue_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100))

    screen.blit(message_text, message_rect)
    screen.blit(instruction_text, instruction_rect)
    screen.blit(difficulty_text, difficulty_rect)
    screen.blit(continue_text, continue_rect)
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                return

def load_questions(difficulty):
    base_path = os.path.dirname(__file__)
    file_path = os.path.join(base_path, f"../questions/{difficulty.lower()}.json")
    with open(file_path, "r") as file:
        questions = json.load(file)
    return questions

def quiz_game(screen, font, difficulty):
    questions = load_questions(difficulty)
    selected_questions = random.sample(questions, 5)  # Select 5 random questions
    score = 0

    for question in selected_questions:
        screen.fill((0, 0, 0))
        question_text = font.render(question["question"], True, (255, 255, 255))
        question_rect = question_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100))
        screen.blit(question_text, question_rect)

        options = question["options"]
        correct_answer = question["answer"]

        for i, option in enumerate(options):
            option_text = font.render(f"{i + 1}. {option}", True, (255, 255, 255))
            option_rect = option_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50 + i * 50))
            screen.blit(option_text, option_rect)

        pygame.display.flip()

        answered = False
        selected_option = None
        while not answered:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4]:
                        selected_option = event.key - pygame.K_1
                        answered = True

        if options[selected_option] == correct_answer:
            score += 1
        else:
            # Highlight incorrect answer in red
            option_text = font.render(f"{selected_option + 1}. {options[selected_option]}", True, (255, 0, 0))
            option_rect = option_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50 + selected_option * 50))
            screen.blit(option_text, option_rect)

        # Highlight correct answer in green
        correct_index = options.index(correct_answer)
        option_text = font.render(f"{correct_index + 1}. {correct_answer}", True, (0, 255, 0))
        option_rect = option_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50 + correct_index * 50))
        screen.blit(option_text, option_rect)

        pygame.display.flip()
        pygame.time.wait(1000)  # Wait for a second

        # Clear event queue to avoid input during the wait period
        pygame.event.clear()

    return score

def quiz_result_screen(screen, font, correct_answers, current_score):
    screen.fill((0, 0, 0))
    result_text = font.render(f"You got {correct_answers} questions right!", True, (255, 255, 255))
    score_text = font.render(f"Current Score: {current_score}", True, (255, 255, 255))
    continue_text = font.render("Press Enter to Continue", True, (255, 255, 255))

    result_rect = result_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
    score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    continue_rect = continue_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))

    screen.blit(result_text, result_rect)
    screen.blit(score_text, score_rect)
    screen.blit(continue_text, continue_rect)
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                return

class PowerUp(pygame.sprite.Sprite):
    def __init__(self, x, y, powerup_type):
        super().__init__()
        self.image = pygame.image.load(f"cyberhunter/images/powerups/{powerup_type}.png")
        self.image = pygame.transform.scale(self.image, (120, 120)) # powerup image size
        self.rect = self.image.get_rect(center=(x, y))
        self.powerup_type = powerup_type

    def update(self):
        self.rect.y += 5
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()

def game_loop(screen, road_image, selected_character_data, all_sprites, enemies, clock, font, SCREEN_WIDTH, SCREEN_HEIGHT, score, difficulty, level=1):
    original_stats = selected_character_data.copy()  # Save original stats
    player_image = pygame.image.load(selected_character_data["image"])
    player = Player(player_image, SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100, selected_character_data["speed"])
    all_sprites.add(player)
    road_y = 0  # Initial position of the road
    score_timer = pygame.time.get_ticks()  # Timer to track score increment
    bullet_timer = pygame.time.get_ticks()  # Timer to control firing rate
    enemy_timer = pygame.time.get_ticks()  # Timer to control enemy spawning
    bullet_speed = 10
    bullet_strength = selected_character_data["strength"]
    bullets = pygame.sprite.Group()
    powerups = pygame.sprite.Group()
    enemy_spawn_interval = 2000  # Spawn an enemy every 1000 milliseconds

    # Load heart image for lives display
    heart_image = pygame.image.load("cyberhunter/images/heart.png")
    heart_image = pygame.transform.scale(heart_image, (35, 35))

    # Initial enemy spawn
    for _ in range(1):  # Spawn an enemy at the start
        enemy_x = random.randint(SCREEN_WIDTH // 4, 3 * SCREEN_WIDTH // 4)
        enemy = Enemy(enemy_x, -50, 5)
        enemies.add(enemy)
        all_sprites.add(enemy)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        keys = pygame.key.get_pressed()
        player.update(keys)
        if keys[pygame.K_SPACE]:
            current_time = pygame.time.get_ticks()
            if current_time - bullet_timer >= 200:
                bullet = Bullet(player.rect.centerx, player.rect.top, bullet_speed, bullet_strength)
                bullets.add(bullet)
                all_sprites.add(bullet)
                bullet_timer = current_time

        # Spawn enemies
        current_time = pygame.time.get_ticks()
        if current_time - enemy_timer >= enemy_spawn_interval:
            enemy_x = random.randint(SCREEN_WIDTH // 4, 3 * SCREEN_WIDTH // 4)
            enemy = Enemy(enemy_x, -50, 5)
            enemies.add(enemy)
            all_sprites.add(enemy)
            enemy_timer = current_time

        # Update positions
        road_y += player.speed
        if road_y >= SCREEN_HEIGHT:
            road_y = 0
        current_time = pygame.time.get_ticks()
        if current_time - score_timer >= 1000:
            score += 10
            score_timer = current_time

        if level == 1 and score >= 500:  # Next level screen at selected score for level 1
            next_level_screen(screen, font, difficulty)
            quiz_score = quiz_game(screen, font, difficulty)
            score += quiz_score * 50  # Add 50 points for each correct answer
            quiz_result_screen(screen, font, quiz_score, score)
            return score, 2  # Return score and next level

        if level == 2 and score >= 1500:  # Next level screen at selected score for level 2
            next_level_screen(screen, font, difficulty)
            quiz_score = quiz_game(screen, font, difficulty)
            score += quiz_score * 50  # Add 50 points for each correct answer
            quiz_result_screen(screen, font, quiz_score, score)
            return score, 3  # Return score and next level

        bullets.update()
        enemies.update()
        powerups.update()

        # Check for collisions
        for bullet in bullets:
            hit_enemies = pygame.sprite.spritecollide(bullet, enemies, False)
            for enemy in hit_enemies:
                print(f"Enemy hit! Health before: {enemy.health}")
                score += enemy.take_damage(bullet.strength)
                bullet.kill()
                print(f"Enemy health after: {enemy.health}")
                if enemy.health <= 0:
                    print("Enemy died!")
                    enemy.kill()
                    if random.random() < 0.4:  # 40% chance to drop a powerup
                        powerup_type = random.choice(["speed", "strength", "agility"])
                        powerup = PowerUp(enemy.rect.centerx, enemy.rect.centery, powerup_type)
                        powerups.add(powerup)
                        all_sprites.add(powerup)

        # Check for player collisions with enemies
        hit_player = pygame.sprite.spritecollide(player, enemies, True)
        if hit_player:
            player.health -= 1
            print(f"Player hit! Health remaining: {player.health}")
            player_hurt_sound.play()
            # Add effect for player hit (e.g., flash screen, sound effect)
            if player.health <= 0:
                print("Player died!")
                player_name = game_over_screen(screen, font, score, selected_character_data["name"])
                print(f"Player Name: {player_name}, Score: {score}, Character: {selected_character_data['name']}")
                selected_character_data.update(original_stats)  # Reset stats to original
                return score, 0  # Return score and game over

        # Check for player collisions with powerups
        hit_powerups = pygame.sprite.spritecollide(player, powerups, True)
        for powerup in hit_powerups:
            if powerup.powerup_type == "speed":
                selected_character_data["speed"] += 1
            elif powerup.powerup_type == "strength":
                selected_character_data["strength"] += 1
            elif powerup.powerup_type == "agility":
                selected_character_data["agility"] += 1
            print(f"Powerup collected: {powerup.powerup_type}")

        # Draw everything
        screen.blit(road_image, (0, road_y - SCREEN_HEIGHT))
        screen.blit(road_image, (0, road_y))
        all_sprites.draw(screen)
        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, 30))
        screen.blit(score_text, score_rect)

        # Draw heart and lives count
        screen.blit(heart_image, (SCREEN_WIDTH - 120, 20))  # Moved to the left
        lives_text = font.render(f"x {player.health}", True, (255, 0, 0))
        screen.blit(lives_text, (SCREEN_WIDTH - 85, 20))  # Moved to the left

        # Draw stats
        stats_text = font.render(f"Speed: {selected_character_data['speed']}", True, (0, 0, 255))
        screen.blit(stats_text, (10, 10))
        stats_text = font.render(f"Strength: {selected_character_data['strength']}", True, (0, 255, 0))
        screen.blit(stats_text, (10, 40))
        stats_text = font.render(f"Agility: {selected_character_data['agility']}", True, (255, 0, 0))
        screen.blit(stats_text, (10, 70))

        pygame.display.flip()
        clock.tick(60)

# main.py
import pygame

# Initialize Pygame
pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('CyberHunter')

# FPS and clock
clock = pygame.time.Clock()

# Load road images
road_image = pygame.image.load("cyberhunter/images/road.png")
road_image = pygame.transform.scale(road_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
road_image2 = pygame.image.load("cyberhunter/images/road2.png")
road_image2 = pygame.transform.scale(road_image2, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Fonts
font = pygame.font.SysFont(None, 55)

# Game loop variables
game_state = "menu"
selected_character = 0

# Sprite groups
all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()

# Main loop
while True:
    if game_state == "menu":
        selected_character, difficulty = menu_loop(screen, font, selected_character)
        game_state = "playing"
        level = 1
        score = 0  # Initialize score
    elif game_state == "playing":
        selected_character_data = characters[selected_character]
        all_sprites.empty()  # Clear sprites before starting a new game
        enemies.empty()
        if level == 1:
            score, next_level = game_loop(screen, road_image, selected_character_data, all_sprites, enemies, clock, font, SCREEN_WIDTH, SCREEN_HEIGHT, score, difficulty, level)
        elif level == 2:
            score, next_level = game_loop(screen, road_image2, selected_character_data, all_sprites, enemies, clock, font, SCREEN_WIDTH, SCREEN_HEIGHT, score, difficulty, level)
        if next_level == 0:
            game_state = "menu"
        else:
            level = next_level
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
player_hurt_sound.set_volume(1.0)  # Set volume to maximum

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, speed, health=20):
        super().__init__()
        self.image = pygame.image.load("cyberhunter/images/cars/enemy.png")
        self.image = pygame.transform.scale(self.image, (100, 150))
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = speed
        self.health = health
        self.max_health = health

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

    def draw_health_bar(self, surface):
        if self.health < self.max_health:
            health_bar_width = self.rect.width
            health_bar_height = 5
            fill = (self.health / self.max_health) * health_bar_width
            outline_rect = pygame.Rect(self.rect.left, self.rect.top - 10, health_bar_width, health_bar_height)
            fill_rect = pygame.Rect(self.rect.left, self.rect.top - 10, fill, health_bar_height)
            pygame.draw.rect(surface, (255, 0, 0), fill_rect)
            pygame.draw.rect(surface, (255, 255, 255), outline_rect, 1)

class EnemyBullet(pygame.sprite.Sprite):
    def __init__(self, x, y, speed=7):
        super().__init__()
        self.image = pygame.Surface((8, 20))
        # Change bullet color to bright yellow
        self.image.fill((255, 255, 102))
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = speed

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()

class Boss(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y, speed=0, health=400)  # Increased health
        self.image = pygame.image.load("cyberhunter/images/cars/boss.png")
        self.image = pygame.transform.scale(self.image, (200, 250))
        self.rect = self.image.get_rect(center=(x, y))
        self.max_health = self.health
        self.shoot_delay = 1200  # milliseconds between shots
        self.last_shot = pygame.time.get_ticks()
        self.target_y = 60  # Higher position
        self.move_direction = 1
        self.move_speed = 2
        self.left_bound = SCREEN_WIDTH // 4
        self.right_bound = SCREEN_WIDTH * 3 // 4

    def update(self):
        # Move boss to target_y smoothly if not already there
        if self.rect.y < self.target_y:
            self.rect.y += 2
            if self.rect.y > self.target_y:
                self.rect.y = self.target_y
        else:
            # Move left and right within bounds
            self.rect.x += self.move_direction * self.move_speed
            if self.rect.right >= self.right_bound:
                self.rect.right = self.right_bound
                self.move_direction = -1
            elif self.rect.left <= self.left_bound:
                self.rect.left = self.left_bound
                self.move_direction = 1

    def try_shoot(self, enemy_bullets_group):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            bullet = EnemyBullet(self.rect.centerx, self.rect.bottom)
            enemy_bullets_group.add(bullet)
            self.last_shot = now

    def draw_health_bar(self, surface):
        bar_width = 600
        bar_height = 30
        x = (SCREEN_WIDTH - bar_width) // 2
        y = 20
        fill = int((self.health / self.max_health) * bar_width)
        pygame.draw.rect(surface, (255, 0, 0), (x, y, fill, bar_height))
        pygame.draw.rect(surface, (255, 255, 255), (x, y, bar_width, bar_height), 3)

# menu.py
import pygame
import sys

def draw_text_with_outline(surface, text, font, color, x, y, outline_color=(0,0,0), outline_width=2):
    """Draw text with an outline for better readability."""
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    # Draw outline by rendering text in outline_color around the main text
    for dx in range(-outline_width, outline_width+1):
        for dy in range(-outline_width, outline_width+1):
            if dx != 0 or dy != 0:
                outline_text = font.render(text, True, outline_color)
                outline_rect = outline_text.get_rect()
                outline_rect.topleft = (x + dx, y + dy)
                surface.blit(outline_text, outline_rect)
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

    # Initialize joystick
    joystick = None
    if pygame.joystick.get_count() > 0:
        joystick = pygame.joystick.Joystick(0)
        joystick.init()

    last_axis_move_time = 0  # Track the last time the joystick axis was moved

    while True:
        screen.fill((0, 0, 0))
        
        # Draw the menu background image
        screen.blit(menu_background, (0, 0))
        
        # Options Positioning
        center_x = SCREEN_WIDTH // 2.25 
        bottom_y = SCREEN_HEIGHT - 250

        # Display "Character :" label
        draw_text_with_outline(screen, "Character :", font, (255, 255, 255), center_x - 150, bottom_y)
        
        # Display selected character
        character = characters[selected_character]
        color = character["color"]
        draw_text_with_outline(screen, character["name"], font, color, center_x + 100, bottom_y)

        # Display character stats
        max_stat_value = 10  # Assuming max value for any stat is 10
        stat_bar_width = 200
        stat_bar_height = 20
        stat_y_offset = 30

        draw_stat_bar(screen, center_x - 150, bottom_y + stat_y_offset, stat_bar_width, stat_bar_height, character["speed"], max_stat_value, (0, 0, 255))
        draw_text_with_outline(screen, "Speed", font, (255, 255, 255), center_x - 150 + stat_bar_width + 10, bottom_y + stat_y_offset)

        draw_stat_bar(screen, center_x - 150, bottom_y + stat_y_offset * 2, stat_bar_width, stat_bar_height, character["strength"], max_stat_value, (0, 255, 0))
        draw_text_with_outline(screen, "Strength", font, (255, 255, 255), center_x - 150 + stat_bar_width + 10, bottom_y + stat_y_offset * 2)

        draw_stat_bar(screen, center_x - 150, bottom_y + stat_y_offset * 3, stat_bar_width, stat_bar_height, character["agility"], max_stat_value, (255, 0, 0))
        draw_text_with_outline(screen, "Agility", font, (255, 255, 255), center_x - 150 + stat_bar_width + 10, bottom_y + stat_y_offset * 3)

        # Display difficulty setting
        draw_text_with_outline(screen, "Question Difficulty: " + difficulty, font, (255, 255, 255), center_x - 150, bottom_y + stat_y_offset * 4 + 30)
        draw_text_with_outline(screen, "Press GREEN to Start", font, (255, 255, 255), center_x - 150, bottom_y + stat_y_offset * 4 + 90)
        draw_text_with_outline(screen, "Press Esc to Exit", font, (255, 255, 255), center_x - 150, bottom_y + stat_y_offset * 4 + 150)

        pygame.display.flip()

        current_time = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    selected_character = (selected_character - 1) % len(characters)
                elif event.key == pygame.K_RIGHT:
                    selected_character = (selected_character + 1) % len(characters)
                elif event.key == pygame.K_UP:
                    selected_difficulty = (selected_difficulty - 1) % len(difficulties)
                    difficulty = difficulties[selected_difficulty]
                elif event.key == pygame.K_DOWN:
                    selected_difficulty = (selected_difficulty + 1) % len(difficulties)
                    difficulty = difficulties[selected_difficulty]
                elif event.key == pygame.K_RETURN:
                    pygame.mixer.music.stop()  # Stop the music when starting the game
                    return selected_character, difficulty
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

            elif event.type == pygame.JOYBUTTONDOWN:
                if event.button == 10:  # Button 1
                    selected_character = (selected_character - 1) % len(characters)
                elif event.button == 9:  # Button 2
                    selected_character = (selected_character + 1) % len(characters)
                elif event.button == 1:  # Button 3
                    pygame.mixer.music.stop()  # Stop the music when starting the game
                    return selected_character, difficulty
                elif event.button == 3:  # Button 4
                    selected_difficulty = (selected_difficulty + 1) % len(difficulties)
                    difficulty = difficulties[selected_difficulty]
                elif event.button == 8:  # Start button
                    pygame.mixer.music.stop()  # Stop the music when starting the game
                    return selected_character, difficulty
                elif event.button == 6:  # Back button
                    pygame.quit()
                    sys.exit()

        if joystick:
            axis_x = joystick.get_axis(0)
            axis_y = joystick.get_axis(1)
            if current_time - last_axis_move_time > 100:  # 100ms delay
                if axis_x < -0.1:
                    selected_character = (selected_character - 1) % len(characters)
                    last_axis_move_time = current_time
                elif axis_x > 0.1:
                    selected_character = (selected_character + 1) % len(characters)
                    last_axis_move_time = current_time
                if axis_y < -0.1:
                    selected_difficulty = (selected_difficulty - 1) % len(difficulties)
                    difficulty = difficulties[selected_difficulty]
                    last_axis_move_time = current_time
                elif axis_y > 0.1:
                    selected_difficulty = (selected_difficulty + 1) % len(difficulties)
                    difficulty = difficulties[selected_difficulty]
                    last_axis_move_time = current_time

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
    def __init__(self, image, x, y, speed, strength, agility):
        super().__init__()
        self.image = pygame.transform.scale(image, (100, 150))
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = speed
        self.strength = strength
        self.agility = agility
        self.health = 5

    def update(self, keys, joystick=None):
        if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and self.rect.left > 0:
            self.rect.x -= self.speed
        if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and self.rect.right < SCREEN_WIDTH:
            self.rect.x += self.speed
        if (keys[pygame.K_UP] or keys[pygame.K_w]) and self.rect.top > 0:
            self.rect.y -= self.speed
        if (keys[pygame.K_DOWN] or keys[pygame.K_s]) and self.rect.bottom < SCREEN_HEIGHT:
            self.rect.y += self.speed

        if joystick:
            axis_x = joystick.get_axis(0)
            axis_y = joystick.get_axis(1)
            if axis_x < -0.1 and self.rect.left > 0:
                self.rect.x -= self.speed
            if axis_x > 0.1 and self.rect.right < SCREEN_WIDTH:
                self.rect.x += self.speed
            if axis_y < -0.1 and self.rect.top > 0:
                self.rect.y -= self.speed
            if axis_y > 0.1 and self.rect.bottom < SCREEN_HEIGHT:
                self.rect.y += self.speed

    def take_damage(self, damage):
        self.health -= damage
        print(f"Player took damage: {damage}, health left: {self.health}")  # Debug print
        
        if self.health <= 0:
            self.kill()

    def update_stats(self, speed, strength, agility):
        self.speed = speed
        self.strength = strength
        self.agility = agility

def game_over_screen(screen, font, score, character_name, selected_character_data, original_stats):
    screen.fill((0, 0, 0))
    # Use draw_text_with_outline for all text
    game_over_text = font.render("Game Over", True, (255, 0, 0))
    score_text = font.render(f"Final Score: {score}", True, (255, 255, 255))
    enter_name_text = font.render("Enter your name:", True, (255, 255, 255))
    continue_text = font.render("Press RED to Continue", True, (255, 255, 255))

    game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100))
    score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
    enter_name_rect = enter_name_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    continue_rect = continue_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100))

    name = ""
    input_active = True
    button_delay = 500  # 500ms delay
    last_button_press_time = 0

    while input_active:
        current_time = pygame.time.get_ticks()
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
            elif event.type == pygame.JOYBUTTONDOWN and event.button == 2:  # Button 2 to continue
                if current_time - last_button_press_time > button_delay:
                    input_active = False
                    last_button_press_time = current_time

        screen.fill((0, 0, 0))
        draw_text_with_outline(screen, "Game Over", font, (255, 0, 0), game_over_rect.left, game_over_rect.top)
        draw_text_with_outline(screen, f"Final Score: {score}", font, (255, 255, 255), score_rect.left, score_rect.top)
        draw_text_with_outline(screen, "Enter your name:", font, (255, 255, 255), enter_name_rect.left, enter_name_rect.top)
        name_text = font.render(name, True, (255, 255, 255))
        name_rect = name_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
        draw_text_with_outline(screen, name, font, (255, 255, 255), name_rect.left, name_rect.top)
        draw_text_with_outline(screen, "Press RED to Continue", font, (255, 255, 255), continue_rect.left, continue_rect.top)
        pygame.display.flip()

    # Save the name, score, current time, and character name to a file
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("scores.txt", "a") as file:
        file.write(f"Name: {name}, Score: {score}, Character: {character_name}, Time: {current_time}\n")

    # Print the time in the terminal
    print(f"Game Over at: {current_time}")

    # Reset character stats to original
    selected_character_data.update(original_stats)

    return name

def next_level_screen(screen, font, difficulty):
    screen.fill((0, 0, 0))
    # Use draw_text_with_outline for all text
    message_text = font.render("You successfully beat this stage!", True, (255, 255, 255))
    instruction_text = font.render("Answer these questions to proceed to the next level", True, (255, 255, 255))
    difficulty_text = font.render(f"Difficulty: {difficulty}", True, (255, 255, 255))
    continue_text = font.render("Press RED to Continue", True, (255, 255, 255))

    message_rect = message_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100))
    instruction_rect = instruction_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
    difficulty_rect = difficulty_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    continue_rect = continue_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100))

    draw_text_with_outline(screen, "You successfully beat this stage!", font, (255, 255, 255), message_rect.left, message_rect.top)
    draw_text_with_outline(screen, "Answer these questions to proceed to the next level", font, (255, 255, 255), instruction_rect.left, instruction_rect.top)
    draw_text_with_outline(screen, f"Difficulty: {difficulty}", font, (255, 255, 255), difficulty_rect.left, difficulty_rect.top)
    draw_text_with_outline(screen, "Press RED to Continue", font, (255, 255, 255), continue_rect.left, continue_rect.top)
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                return
            elif event.type == pygame.JOYBUTTONDOWN and event.button == 2:  # Button 2 to continue
                return

def load_questions(difficulty):
    base_path = os.path.dirname(__file__)
    file_path = os.path.join(base_path, f"../questions/{difficulty.lower()}.json")
    with open(file_path, "r") as file:
        questions = json.load(file)
    return questions

def quiz_game(screen, font, difficulty):
    # Load quiz music
    pygame.mixer.music.load("cyberhunter/audio/quiz.wav")
    pygame.mixer.music.play(-1)  # Loop the music indefinitely

    questions = load_questions(difficulty)
    selected_questions = random.sample(questions, 5)  # Select 5 random questions
    score = 0

    for question in selected_questions:
        screen.fill((0, 0, 0))
        # --- Split question into two lines and position higher ---
        q_text = question["question"]
        words = q_text.split()
        if len(words) > 6:
            mid = len(words) // 2
            line1 = " ".join(words[:mid])
            line2 = " ".join(words[mid:])
        else:
            line1 = q_text
            line2 = ""
        # Position higher on the screen
        y_base = SCREEN_HEIGHT // 2 - 170
        line_spacing = 40
        line1_rect = font.render(line1, True, (255, 255, 255)).get_rect(center=(SCREEN_WIDTH // 2, y_base))
        draw_text_with_outline(screen, line1, font, (255, 255, 255), line1_rect.left, line1_rect.top)
        if line2:
            line2_rect = font.render(line2, True, (255, 255, 255)).get_rect(center=(SCREEN_WIDTH // 2, y_base + line_spacing))
            draw_text_with_outline(screen, line2, font, (255, 255, 255), line2_rect.left, line2_rect.top)

        options = question["options"]
        correct_answer = question["answer"]
        colors = [(0, 0, 255), (0, 255, 0), (255, 0, 0), (255, 255, 0)]  # Blue, Green, Red, Yellow

        option_rects = []
        # Lower the options further down the screen
        options_start_y = y_base + 130  # Increased from 70 to 130
        for i, option in enumerate(options):
            option_text = font.render(f"{i + 1}. {option}", True, colors[i])
            option_rect = option_text.get_rect(center=(SCREEN_WIDTH // 2, options_start_y + i * 50))
            draw_text_with_outline(screen, f"{i + 1}. {option}", font, colors[i], option_rect.left, option_rect.top)
            option_rects.append(option_rect)

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
                elif event.type == pygame.JOYBUTTONDOWN:
                    if event.button in [0, 1, 2, 3]:  # Buttons 1-4
                        selected_option = event.button
                        answered = True

        if options[selected_option] == correct_answer:
            score += 1
            pygame.draw.rect(screen, (0, 255, 0), (option_rects[selected_option].left - 10, option_rects[selected_option].top - 10, option_rects[selected_option].width + 20, option_rects[selected_option].height + 20))
        else:
            pygame.draw.rect(screen, (255, 0, 0), (option_rects[selected_option].left - 10, option_rects[selected_option].top - 10, option_rects[selected_option].width + 20, option_rects[selected_option].height + 20))
        correct_index = options.index(correct_answer)
        pygame.draw.rect(screen, (0, 255, 0), (option_rects[correct_index].left - 10, option_rects[correct_index].top - 10, option_rects[correct_index].width + 20, option_rects[correct_index].height + 20))
        for i, option in enumerate(options):
            draw_text_with_outline(screen, f"{i + 1}. {option}", font, (0, 0, 0), option_rects[i].left, option_rects[i].top)
        pygame.display.flip()
        pygame.time.wait(1000)
        pygame.event.clear()
    return score

def quiz_result_screen(screen, font, correct_answers, current_score):
    screen.fill((0, 0, 0))
    result_text = font.render(f"You got {correct_answers} questions right!", True, (255, 255, 255))
    score_text = font.render(f"Current Score: {current_score}", True, (255, 255, 255))
    continue_text = font.render("Press RED to Continue", True, (255, 255, 255))

    result_rect = result_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
    score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    continue_rect = continue_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))

    draw_text_with_outline(screen, f"You got {correct_answers} questions right!", font, (255, 255, 255), result_rect.left, result_rect.top)
    draw_text_with_outline(screen, f"Current Score: {current_score}", font, (255, 255, 255), score_rect.left, score_rect.top)
    draw_text_with_outline(screen, "Press RED to Continue", font, (255, 255, 255), continue_rect.left, continue_rect.top)
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                return
            elif event.type == pygame.JOYBUTTONDOWN and event.button == 2:  # Button 2 to continue
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

def reset_character_stats():
    original_stats = [
        {"name": "Daniel", "color": (0, 255, 0), "speed": 6, "strength": 7, "agility": 7, "image": "cyberhunter/images/cars/daniel_car.png"},
        {"name": "Mo", "color": (128, 0, 128), "speed": 8, "strength": 6, "agility": 6, "image": "cyberhunter/images/cars/mo_car.png"},
        {"name": "Rene", "color": (0, 0, 255), "speed": 6, "strength": 8, "agility": 6, "image": "cyberhunter/images/cars/rene_car.png"},
        {"name": "Owen", "color": (255, 105, 180), "speed": 7, "strength": 7, "agility": 6, "image": "cyberhunter/images/cars/owen_car.png"}
    ]
    for i, character in enumerate(characters):
        character.update(original_stats[i])

def game_completed_screen(screen, font, score, character_name, selected_character_data, original_stats):
    screen.fill((0, 0, 0))
    completed_text = font.render("Game Completed!", True, (0, 255, 0))
    score_text = font.render(f"Final Score: {score}", True, (255, 255, 255))
    enter_name_text = font.render("Enter your name:", True, (255, 255, 255))
    continue_text = font.render("Press RED to Continue", True, (255, 255, 255))

    completed_rect = completed_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100))
    score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
    enter_name_rect = enter_name_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    continue_rect = continue_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100))

    name = ""
    input_active = True
    button_delay = 500  # 500ms delay
    last_button_press_time = 0

    while input_active:
        current_time = pygame.time.get_ticks()
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
            elif event.type == pygame.JOYBUTTONDOWN and event.button == 2:  # Button 2 to continue
                if current_time - last_button_press_time > button_delay:
                    input_active = False
                    last_button_press_time = current_time

        screen.fill((0, 0, 0))
        draw_text_with_outline(screen, "Game Completed!", font, (0, 255, 0), completed_rect.left, completed_rect.top)
        draw_text_with_outline(screen, f"Final Score: {score}", font, (255, 255, 255), score_rect.left, score_rect.top)
        draw_text_with_outline(screen, "Enter your name:", font, (255, 255, 255), enter_name_rect.left, enter_name_rect.top)
        draw_text_with_outline(screen, name, font, (255, 255, 255), SCREEN_WIDTH // 2 - font.size(name)[0] // 2, SCREEN_HEIGHT // 2 + 50)
        draw_text_with_outline(screen, "Press RED to Continue", font, (255, 255, 255), continue_rect.left, continue_rect.top)
        pygame.display.flip()

    # Save the name, score, current time, and character name to a file
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("scores.txt", "a") as file:
        file.write(f"Name: {name}, Score: {score}, Character: {character_name}, Time: {current_time}\n")

    # Print the time in the terminal
    print(f"Game Completed at: {current_time}")

    # Reset character stats to original
    reset_character_stats()

    return name

def game_loop(screen, road_image, selected_character_data, all_sprites, enemies, clock, font, SCREEN_WIDTH, SCREEN_HEIGHT, score, difficulty, level=1):
    original_stats = selected_character_data.copy()  # Save original stats
    player_image = pygame.image.load(selected_character_data["image"])
    player = Player(player_image, SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100, selected_character_data["speed"], selected_character_data["strength"], selected_character_data["agility"])
    all_sprites.add(player)
    road_y = 0  # Initial position of the road
    score_timer = pygame.time.get_ticks()  # Timer to track score increment
    bullet_timer = pygame.time.get_ticks()  # Timer to control firing rate
    enemy_timer = pygame.time.get_ticks()  # Timer to control enemy spawning
    bullet_speed = 10
    bullet_strength = selected_character_data["strength"]
    bullets = pygame.sprite.Group()
    powerups = pygame.sprite.Group()
    enemy_bullets = pygame.sprite.Group()  # Add this line
    enemy_spawn_interval = 1500 if level == 1 else 2000  # Default spawn interval
    if level == 2:
        enemy_spawn_interval = 2000  # Spawn interval for level 2
    elif level == 3:
        enemy_spawn_interval = 2500  # Spawn interval for level 3
    elif level == 4:
        enemy_spawn_interval = 3000  # Spawn interval for level 4

    # Load heart image for lives display
    heart_image = pygame.image.load("cyberhunter/images/heart.png")
    heart_image = pygame.transform.scale(heart_image, (35, 35))

    # Load level music
    if level == 1:
        pygame.mixer.music.load("cyberhunter/audio/lvl1.wav")
    elif level == 2:
        pygame.mixer.music.load("cyberhunter/audio/lvl2.wav")
    elif level == 3:
        pygame.mixer.music.load("cyberhunter/audio/lvl3.wav")
    elif level == 4:
        pygame.mixer.music.load("cyberhunter/audio/lvl4.wav")
    pygame.mixer.music.set_volume(0.25)  # Set volume to quarter
    pygame.mixer.music.play(-1)  # Loop the music indefinitely

    # Initialize joystick
    joystick = None
    if pygame.joystick.get_count() > 0:
        joystick = pygame.joystick.Joystick(0)
        joystick.init()

    # Initial enemy spawn
    for _ in range(1):  # Spawn an enemy at the start
        enemy_x = random.randint(SCREEN_WIDTH // 4, 3 * SCREEN_WIDTH // 4)
        if level == 1:
            enemy_health = 20
        elif level == 2:
            enemy_health = 25
        elif level == 3:
            enemy_health = 30
        elif level == 4:
            enemy_health = 35
        enemy = Enemy(enemy_x, -50, 5, enemy_health)
        enemies.add(enemy)
        all_sprites.add(enemy)

    boss_spawned = False
    boss_defeated = False
    boss = None

    # Add these lines
    boss_warning_shown = False
    boss_warning_time = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        keys = pygame.key.get_pressed()
        player.update(keys, joystick)
        if keys[pygame.K_SPACE] or (joystick and (joystick.get_button(0) or joystick.get_button(2))):  # Button 3 to shoot
            current_time = pygame.time.get_ticks()
            if current_time - bullet_timer >= 200:
                bullet = Bullet(player.rect.centerx, player.rect.top, bullet_speed, player.strength)
                bullets.add(bullet)
                all_sprites.add(bullet)
                bullet_timer = current_time

        # Spawn enemies (skip if boss is spawned in level 4)
        current_time = pygame.time.get_ticks()
        if level == 4 and score >= 2500 and not boss_spawned:
            if not boss_warning_shown:
                boss_warning_time = pygame.time.get_ticks()
                boss_warning_shown = True
                continue  # Skip the rest of the loop to show the warning
            elif pygame.time.get_ticks() - boss_warning_time < 2000:
                # Make warning less chaotic: single color, slow shake, centered
                warning_font = arcade_font
                shake_amount = 8
                # Slow shake using sine wave based on time
                import math
                t = pygame.time.get_ticks() / 200.0
                shake_x = int(math.sin(t) * shake_amount)
                shake_y = int(math.cos(t) * shake_amount)
                warning_text = warning_font.render("!!! WARNING !!!", True, (255, 255, 0))  # Bright yellow
                warning_rect = warning_text.get_rect(center=(SCREEN_WIDTH // 2 + shake_x, SCREEN_HEIGHT // 2 - 20 + shake_y))
                screen.fill((0,0,0))
                screen.blit(warning_text, warning_rect)
                warning_text2 = warning_font.render("BOSS INCOMING!", True, (255, 255, 0))
                warning_rect2 = warning_text2.get_rect(center=(SCREEN_WIDTH // 2 - shake_x, SCREEN_HEIGHT // 2 + 20 - shake_y))
                screen.blit(warning_text2, warning_rect2)
                pygame.display.flip()
                continue
            else:
                # After warning, spawn the boss
                boss = Boss(SCREEN_WIDTH // 2, -125)
                enemies.add(boss)
                all_sprites.add(boss)
                boss_spawned = True

        if not (level == 4 and boss_spawned):
            if current_time - enemy_timer >= enemy_spawn_interval:
                enemy_x = random.randint(SCREEN_WIDTH // 4, 3 * SCREEN_WIDTH // 4)
                if level == 1:
                    enemy_health = 20
                elif level == 2:
                    enemy_health = 25
                elif level == 3:
                    enemy_health = 30
                elif level == 4:
                    enemy_health = 35
                enemy = Enemy(enemy_x, -50, 5, enemy_health)
                enemies.add(enemy)
                all_sprites.add(enemy)
                enemy_timer = current_time

        # Update positions
        # Always move the road, even during boss fight
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

        if level == 2 and score >= 1250:  # Next level screen at selected score for level 2
            next_level_screen(screen, font, difficulty)
            quiz_score = quiz_game(screen, font, difficulty)
            score += quiz_score * 50  # Add 50 points for each correct answer
            quiz_result_screen(screen, font, quiz_score, score)
            return score, 3  # Return score and next level

        if level == 3 and score >= 2000:  # Next level screen at selected score for level 3
            next_level_screen(screen, font, difficulty)
            quiz_score = quiz_game(screen, font, difficulty)
            score += quiz_score * 50  # Add 50 points for each correct answer
            quiz_result_screen(screen, font, quiz_score, score)
            return score, 4  # Return score and next level

        bullets.update()
        enemies.update()
        powerups.update()
        enemy_bullets.update()  # Update boss bullets

        # Boss fires bullets
        if boss_spawned and boss in enemies:
            boss.try_shoot(enemy_bullets)

        # Check for collisions
        for bullet in bullets:
            hit_enemies = pygame.sprite.spritecollide(bullet, enemies, False)
            for enemy in hit_enemies:
                print(f"Enemy hit! Health before: {enemy.health}")
                score += enemy.take_damage(bullet.strength)
                bullet.kill()
                print(f"Enemy health after: {enemy.health}")
                if enemy.health <= 0:
                    print("Enemy died Successfully!")
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
                player_name = game_over_screen(screen, font, score, selected_character_data["name"], selected_character_data, original_stats)
                print(f"Player Name: {player_name}, Score: {score}, Character: {selected_character_data['name']}")
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
            player.update_stats(selected_character_data["speed"], selected_character_data["strength"], selected_character_data["agility"])

        # Check for collisions between player and boss bullets
        if pygame.sprite.spritecollide(player, enemy_bullets, True):
            player.health -= 1
            player_hurt_sound.play()
            if player.health <= 0:
                player_name = game_over_screen(screen, font, score, selected_character_data["name"], selected_character_data, original_stats)
                return score, 0

        # Draw everything
        screen.blit(road_image, (0, road_y - SCREEN_HEIGHT))
        screen.blit(road_image, (0, road_y))
        all_sprites.draw(screen)
        enemy_bullets.draw(screen)  # Draw boss bullets

        # Define score_rect before using it
        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, 30))
        draw_text_with_outline(screen, f"Score: {score}", font, (255, 255, 255), score_rect.left, score_rect.top)

        # Draw heart and lives count
        screen.blit(heart_image, (SCREEN_WIDTH - 120, 20))  # Moved to the left
        draw_text_with_outline(screen, f"x {player.health}", font, (255, 0, 0), SCREEN_WIDTH - 85, 20)  # Moved to the left

        # Draw stats
        draw_text_with_outline(screen, f"Speed: {selected_character_data['speed']}", font, (0, 0, 255), 10, 10)
        draw_text_with_outline(screen, f"Strength: {selected_character_data['strength']}", font, (0, 255, 0), 10, 40)
        draw_text_with_outline(screen, f"Agility: {selected_character_data['agility']}", font, (255, 0, 0), 10, 70)

        # Draw enemy health bars
        for enemy in enemies:
            if isinstance(enemy, Boss):
                enemy.draw_health_bar(screen)
            else:
                enemy.draw_health_bar(screen)

        # Boss defeat check (add this after all updates and collision checks)
        if level == 4 and boss_spawned and boss not in enemies:
            game_completed_screen(screen, font, score, selected_character_data["name"], selected_character_data, original_stats)
            return score, 0  # Game completed

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
road_image3 = pygame.image.load("cyberhunter/images/road3.png")  
road_image3 = pygame.transform.scale(road_image3, (SCREEN_WIDTH, SCREEN_HEIGHT))
road_image4 = pygame.image.load("cyberhunter/images/road4.png")  # Load road4.png for level 4
road_image4 = pygame.transform.scale(road_image4, (SCREEN_WIDTH, SCREEN_HEIGHT))


# Fonts
arcade_font = pygame.font.Font("cyberhunter/fonts/PressStart2P.ttf", 22)
font = arcade_font  # Use this everywhere instead of SysFont or None

# For smaller text, you can use:
arcade_font_small = pygame.font.Font("cyberhunter/fonts/PressStart2P.ttf", 12)

# Game loop variables
game_state = "menu"
selected_character = 0

# Sprite groups
all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()

# Main loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F11:
                fullscreen = not fullscreen
                if fullscreen:
                    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
                else:
                    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
                pygame.display.flip()  # Update the display mode
    if game_state == "menu":
        selected_character, difficulty = menu_loop(screen, font, selected_character)
        reset_character_stats()  # Reset character stats when entering the game
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
        elif level == 3:
            score, next_level = game_loop(screen, road_image3, selected_character_data, all_sprites, enemies, clock, font, SCREEN_WIDTH, SCREEN_HEIGHT, score, difficulty, level)
        elif level == 4:
            score, next_level = game_loop(screen, road_image4, selected_character_data, all_sprites, enemies, clock, font, SCREEN_WIDTH, SCREEN_HEIGHT, score, difficulty, level)
        if next_level == 0:
            game_state = "menu"
        else:
            level = next_level
    pygame.display.flip()  # Ensure the display is updated every frame
    clock.tick(60)  # Maintain the frame rate
import pygame
from config import SCREEN_WIDTH, SCREEN_HEIGHT, characters
from menu import menu_loop
from game import game_loop

# Initialize Pygame
pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Cyber Hunter')

# FPS and clock
clock = pygame.time.Clock()

# Load road image
road_image = pygame.image.load("../images/road.png")
road_image = pygame.transform.scale(road_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

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
    elif game_state == "playing":
        selected_character_data = characters[selected_character]
        all_sprites.empty()  # Clear sprites before starting a new game
        enemies.empty()
        score = 0  # Initialize score
        game_state = game_loop(screen, road_image, selected_character_data, all_sprites, enemies, clock, font, SCREEN_WIDTH, SCREEN_HEIGHT, score)
        
import pygame
import sys
from config import characters, SCREEN_WIDTH, SCREEN_HEIGHT

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
    menu_background = pygame.image.load("../images/menubkg.png")
    menu_background = pygame.transform.scale(menu_background, (SCREEN_WIDTH, SCREEN_HEIGHT))

    # Load and play menu music
    pygame.mixer.music.load("../audio/menumsc.ogg")
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

        draw_stat_bar(screen, center_x - 150, bottom_y + stat_y_offset, stat_bar_width, stat_bar_height, character["speed"], max_stat_value, (0, 255, 0))
        draw_text(screen, "Speed", font, (255, 255, 255), center_x - 150 + stat_bar_width + 10, bottom_y + stat_y_offset)

        draw_stat_bar(screen, center_x - 150, bottom_y + stat_y_offset * 2, stat_bar_width, stat_bar_height, character["strength"], max_stat_value, (255, 0, 0))
        draw_text(screen, "Strength", font, (255, 255, 255), center_x - 150 + stat_bar_width + 10, bottom_y + stat_y_offset * 2)

        draw_stat_bar(screen, center_x - 150, bottom_y + stat_y_offset * 3, stat_bar_width, stat_bar_height, character["agility"], max_stat_value, (0, 0, 255))
        draw_text(screen, "Agility", font, (255, 255, 255), center_x - 150 + stat_bar_width + 10, bottom_y + stat_y_offset * 3)

        # Display difficulty setting
        draw_text(screen, "Difficulty: " + difficulty, font, (255, 255, 255), center_x - 150, bottom_y + stat_y_offset * 4 + 30)
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
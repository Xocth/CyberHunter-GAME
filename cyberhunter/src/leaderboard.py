import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Leaderboard')

# Fonts
font = pygame.font.SysFont(None, 75)  # Increased font size for the title
small_font = pygame.font.SysFont(None, 45)  # Increased font size for the entries

def read_scores(file_path):
    scores = []
    try:
        with open(file_path, "r") as file:
            for line in file:
                parts = line.strip().split(", ")
                if len(parts) == 4:
                    try:
                        name = parts[0].split(": ")[1]
                        score = int(parts[1].split(": ")[1])
                        character = parts[2].split(": ")[1]
                        time = parts[3].split(": ")[1]
                        scores.append((name, score, character, time))
                    except (ValueError, IndexError) as e:
                        print(f"Skipping line due to error: {e}")
                        continue
                else:
                    print(f"Skipping line due to incorrect format: {line.strip()}")
    except FileNotFoundError as e:
        print(f"File not found: {e}")
    return scores

def display_leaderboard(screen, font, small_font, scores):
    screen.fill((0, 0, 0))
    title_text = font.render("Leaderboard", True, (255, 255, 255))
    title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 50))
    screen.blit(title_text, title_rect)

    y_offset = 150
    for i, (name, score, character, time) in enumerate(scores[:10]):
        # Extract only the time part (HH:MM:SS) from the datetime string
        time_only = time.split(" ")[1]
        entry_text = small_font.render(f"{i + 1}. {name} - {score} - Character used: {character} - {time_only}", True, (255, 255, 255))
        entry_rect = entry_text.get_rect(center=(SCREEN_WIDTH // 2, y_offset))
        screen.blit(entry_text, entry_rect)
        y_offset += 50  # Increased spacing between entries

    pygame.display.flip()

def main():
    scores = read_scores("scores.txt")
    scores.sort(key=lambda x: x[1], reverse=True)

    # Debug print statements
    print("Scores read from file:")
    for score in scores:
        print(score)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        display_leaderboard(screen, font, small_font, scores)

if __name__ == "__main__":
    main()
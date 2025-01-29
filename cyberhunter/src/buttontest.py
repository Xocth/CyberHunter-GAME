import pygame

def main():
    pygame.init()
    
    # Initialize joystick
    pygame.joystick.init()
    if pygame.joystick.get_count() == 0:
        print("No joystick detected!")
        return
    
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    print(f"Detected joystick: {joystick.get_name()}")
    
    # Create a simple window
    screen = pygame.display.set_mode((400, 300))
    pygame.display.set_caption("Joystick Test")
    font = pygame.font.Font(None, 30)
    clock = pygame.time.Clock()
    
    running = True
    while running:
        screen.fill((0, 0, 0))
        events = pygame.event.get()
        
        for event in events:
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.JOYBUTTONDOWN:
                print(f"Button {event.button} pressed")
            elif event.type == pygame.JOYBUTTONUP:
                print(f"Button {event.button} released")
            elif event.type == pygame.JOYAXISMOTION:
                print(f"Axis {event.axis} moved to {event.value:.2f}")
            elif event.type == pygame.JOYHATMOTION:
                print(f"D-Pad moved to {event.value}")
        
        # Render some text on screen
        text = font.render("Press buttons or move joystick", True, (255, 255, 255))
        screen.blit(text, (50, 130))
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()

if __name__ == "__main__":
    main()

import pygame
import sys
from Carviewer_global import *

def fade_in_text(surface, text, font, color, center, alpha):
    text_surface = font.render(text, True, color)
    text_surface.set_alpha(alpha)
    text_rect = text_surface.get_rect(center=center)
    surface.blit(text_surface, text_rect)

font_extra_large = pygame.font.Font(None, 64)
font_medium = pygame.font.Font(None, 48)

# Clock
clock = pygame.time.Clock()
FPS = 60

# Animation settings
car_speed = 6
pause_frames = 60
fade_frames = 60

frame = 0

alpha = 0

def show_intro():
    phase = "drive_in"

    # Load and scale car image (original is 570x403)
    original_car = pygame.image.load("fiesta_mk6.png").convert_alpha()
    car_width = 400
    car_height = int(403 * (car_width / 570))  # maintain aspect ratio
    car_image = pygame.transform.smoothscale(original_car, (car_width, car_height))
    car_x = -car_image.get_width()
    car_y = HEIGHT // 2 - car_image.get_height() // 2

    # Main loop
    running = True
    while running:
        screen.fill(BACKGROUND_COLOR)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if phase == "drive_in":
            car_x += car_speed
            if car_x >= WIDTH // 2 - car_image.get_width() // 2:
                car_x = WIDTH // 2 - car_image.get_width() // 2
                phase = "pause"
                frame = 0

        elif phase == "pause":
            frame += 1
            if frame > pause_frames:
                phase = "fade_text"
                frame = 0

        elif phase == "fade_text":
            alpha = min(255, int((frame / fade_frames) * 255))
            # Top title
            fade_in_text(screen, "Car Viewer", font_extra_large, TEXT_COLOR, (WIDTH // 2, car_y - 60), alpha)
            # Under car
            fade_in_text(screen, "Ford Fiesta MK6 Sport", font_medium, TEXT_COLOR, (WIDTH // 2, car_y + car_height + 30), alpha)
            fade_in_text(screen, "Made by Patrick Wildschut", font_small, TEXT_COLOR, (WIDTH // 2, car_y + car_height + 70), alpha)
            frame += 1
            if frame >= fade_frames + 60:
                phase = "done"

        elif phase == "done":
            pygame.time.delay(1200)
            running = False

        # Draw car
        screen.blit(car_image, (car_x, car_y))

        pygame.display.flip()
        clock.tick(FPS)

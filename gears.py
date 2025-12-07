import pygame
import math
from Carviewer_ESP32 import *

def UpdateGears():
    current_speed = GetSpeed()
    GetRPM()
    return [x * current_speed for x in gears]

def gears_screen():
    running = True
    clock = pygame.time.Clock()

    circle_positions = {
        1: (250, 200),
        2: (500, 200),
        3: (750, 200),
        4: (350, 400),
        5: (650, 400),
    }

    rpm_circle_radius = 100

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if back_rect.collidepoint(x, y):
                    return

        gear_rpm = UpdateGears()
        current_speed = int(GetSpeed())

        screen.fill(BACKGROUND_COLOR)

        # ----- Best Gear Calculation -----
        best_gear = None
        best_rpm = None

        for i, rpm in enumerate(gear_rpm, start=1):
            if rpm >= 1250:  # only consider gears above threshold
                if best_rpm is None or rpm < best_rpm:
                    best_rpm = rpm
                    best_gear = i

        best_gear = min(5, best_gear)

        # ----- Title -----
        title_text = font_large.render("Gears", True, TEXT_COLOR)
        screen.blit(title_text, (50, 50))

        # ----- Draw 5 Gear RPM Circles -----
        for gear in range(1, 6):
            rpm = gear_rpm[gear - 1]
            cx, cy = circle_positions[gear]

            # ----- Color Logic -----
            if rpm >= 5000:
                circle_color = (255, 0, 0)  # red
            else:
                circle_color = TEXT_COLOR   # default

            # Draw outer circle
            pygame.draw.circle(screen, circle_color, (cx, cy), rpm_circle_radius, 3)

            # Draw arc
            arc_rect = (
                cx - rpm_circle_radius, cy - rpm_circle_radius,
                rpm_circle_radius * 2, rpm_circle_radius * 2
            )

            start_angle = 3 * math.pi / 2
            end_angle = start_angle - (rpm / 6000) * (2 * math.pi)

            pygame.draw.arc(screen, circle_color, arc_rect, end_angle, start_angle, 10)

            # ----- Gear Number Color Logic -----
            current_gear = GetGear()

            if gear == best_gear:
                gear_number_color = (0, 255, 0)     # GREEN = best gear

            elif gear == current_gear:
                gear_number_color = (0, 128, 255)   # BLUE = current gear

            else:
                gear_number_color = TEXT_COLOR      # normal


            # Draw gear number
            gear_text = font_large.render(str(gear), True, gear_number_color)
            screen.blit(gear_text, gear_text.get_rect(center=(cx, cy - 20)))

            # RPM text under gear
            rpm_text = font_small.render(f"{int(rpm)} RPM", True, TEXT_COLOR)
            screen.blit(rpm_text, rpm_text.get_rect(center=(cx, cy + 40)))

        # ----- Speed Display (bottom-right) -----
        speed_label = font_small.render("Speed:", True, TEXT_COLOR)
        screen.blit(speed_label, (WIDTH - 200, HEIGHT - 120))

        speed_value = font_large.render(f"{current_speed}", True, TEXT_COLOR)
        screen.blit(speed_value, (WIDTH - 200, HEIGHT - 80))

        # ----- Back Button -----
        back_rect = pygame.Rect(50, 500, 200, 50)
        pygame.draw.rect(screen, BUTTON_COLOR, back_rect)
        back_text = font_small.render("Back", True, BUTTON_TEXT_COLOR)
        screen.blit(back_text, back_text.get_rect(center=back_rect.center))

        pygame.display.flip()
        clock.tick(30)

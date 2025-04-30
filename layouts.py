import pygame
import math
from Carviewer_dummy import *


# Function to draw dashboard
def original_dashboard(throttle, speed, rpm, clutch_pressed, brake_pressed):
    screen.fill(BACKGROUND_COLOR)
    
    # Title
    title_text = font_large.render("Ford Fiesta MK6 Sport", True, TEXT_COLOR)
    screen.blit(title_text, (50, 50))
    
    # About Button
    about_button_rect = pygame.Rect(WIDTH - 150, 50, 100, 30)
    pygame.draw.rect(screen, BUTTON_COLOR, about_button_rect)
    tools_text = font_small.render("Tools", True, BUTTON_TEXT_COLOR)
    text_rect = tools_text.get_rect(center=about_button_rect.center)
    screen.blit(tools_text, text_rect)

    # version label
    version_text = font_small.render(f"Version: {settings_json['Program']['version']}", True, TEXT_COLOR)
    
    screen.blit(version_text, (WIDTH // 2 - version_text.get_width() // 2, 550))
    
    # Throttle
    throttle_label = font_small.render("Throttle", True, TEXT_COLOR)
    screen.blit(throttle_label, (50, 150))
    # pygame.draw.rect(screen, BUTTON_COLOR, (250, 150, throttle * 2, 30))

    throttle_circle_radius = 100
    pygame.draw.circle(screen, TEXT_COLOR, (300, 200), throttle_circle_radius, 3)
    pygame.draw.arc(screen, TEXT_COLOR, (200, 100, 200, 200), 3 * math.pi / 2 - (throttle / 100) * 2 * math.pi, 3 * math.pi / 2, 10)


    throttle_text = font_large.render(str(throttle), True, TEXT_COLOR)
    screen.blit(throttle_text, (300 - throttle_text.get_width() / 2, 200 - throttle_text.get_height() / 2))
    percent_text = font_small.render("%", True, TEXT_COLOR)
    screen.blit(percent_text, (325, 190))
    
    # Speed
    speed_label = font_small.render("Speed", True, TEXT_COLOR)
    screen.blit(speed_label, (550, 150))
    
    # Draw speed circle
    speed_circle_radius = 100
    pygame.draw.circle(screen, TEXT_COLOR, (800, 200), speed_circle_radius, 3)
    

    speed_text = None

    if speed > 105:
        speed_text = font_large.render(str(int(speed)), True, RED)
        pygame.draw.arc(screen, RED, (700, 100, 200, 200), 3 * math.pi / 2 - (speed / 200) * 2 * math.pi, 3 * math.pi / 2, 10)
    else:
        speed_text = font_large.render(str(int(speed)), True, TEXT_COLOR)
        pygame.draw.arc(screen, TEXT_COLOR, (700, 100, 200, 200), 3 * math.pi / 2 - (speed / 200) * 2 * math.pi, 3 * math.pi / 2, 10)
    
    screen.blit(speed_text, (800 - speed_text.get_width() / 2, 200 - speed_text.get_height() / 2))
    kmh_text = font_small.render("km/h", True, TEXT_COLOR)
    screen.blit(kmh_text, (775, 225))
    
    # Clutch
    clutch_label = font_small.render("Clutch", True, TEXT_COLOR)
    screen.blit(clutch_label, (50, 375))
    clutch_text = font_small.render("Pressed" if clutch_pressed else "Released", True, RED if clutch_pressed else GREEN)
    screen.blit(clutch_text, (300, 375))
    
    # Brake
    brake_label = font_small.render("Brake", True, TEXT_COLOR)
    screen.blit(brake_label, (550, 375))
    brake_text = font_small.render("Pressed" if brake_pressed else "Released", True, RED if brake_pressed else GREEN)
    screen.blit(brake_text, (800, 375))

    # RPM test
    rpm_label = font_small.render("RPM", True, TEXT_COLOR)
    screen.blit(rpm_label, (412, 475))
    rpm_text = font_small.render(str(rpm), True, RED if rpm > 4500 else TEXT_COLOR)
    screen.blit(rpm_text, (562, 475))
    
    # Draw horizontal lines
    pygame.draw.line(screen, TEXT_COLOR, (50, 330), (950, 330), 2)
    pygame.draw.line(screen, TEXT_COLOR, (50, 450), (950, 450), 2)
    
    # Draw buttons
    button_width = 200
    button_height = 50
    
    pygame.draw.rect(screen, BUTTON_COLOR, (50, 500, button_width, button_height))
    apple_carplay_text = font_small.render("Apple CarPlay", True, BUTTON_TEXT_COLOR)
    text_rect = apple_carplay_text.get_rect(center=(50 + button_width // 2, 500 + button_height // 2))
    screen.blit(apple_carplay_text, text_rect)
    
    pygame.draw.rect(screen, BUTTON_COLOR, (WIDTH - 50 - button_width, 500, button_width, button_height))
    settings_text = font_small.render("Settings", True, BUTTON_TEXT_COLOR)
    text_rect = settings_text.get_rect(center=(WIDTH - 50 - button_width // 2, 500 + button_height // 2))
    screen.blit(settings_text, text_rect)

def fancy_dashboard(throttle, speed, rpm, clutch_pressed, brake_pressed, gear):
    screen.fill(BACKGROUND_COLOR)

    # Title (centered)
    title_surface = font_large.render("Ford Fiesta MK6 Sport", True, TEXT_COLOR)
    screen.blit(title_surface, ((WIDTH - title_surface.get_width()) // 2, 30))

    # Circle positions
    throttle_pos = (250, 180)
    speed_pos = (WIDTH - 250, 180)

    # --- Throttle Circle ---
    pygame.draw.circle(screen, (60, 60, 70), throttle_pos, 100)
    pygame.draw.arc(screen, BLUE, (throttle_pos[0] - 100, throttle_pos[1] - 100, 200, 200),
                    3 * math.pi / 2 - (throttle / 100) * 2 * math.pi, 3 * math.pi / 2, 10)
    throttle_text = font_large.render(f"{throttle}%", True, TEXT_COLOR)
    screen.blit(throttle_text, (throttle_pos[0] - throttle_text.get_width() // 2, throttle_pos[1] - 20))
    throttle_label = font_small.render("Throttle", True, TEXT_COLOR)
    screen.blit(throttle_label, (throttle_pos[0] - throttle_label.get_width() // 2, throttle_pos[1] + 40))

    # --- Gear ---
    rpm_label = font_super_large.render(str(gear) if gear != -1 else "N", True, TEXT_COLOR if rpm < 5000 else RED)
    screen.blit(rpm_label, (WIDTH // 2 - rpm_label.get_width() // 2, 170))

    # --- Speed Circle ---
    pygame.draw.circle(screen, (60, 60, 70), speed_pos, 100)
    pygame.draw.arc(screen, RED, (speed_pos[0] - 100, speed_pos[1] - 100, 200, 200),
                    3 * math.pi / 2 - (speed / 200) * 2 * math.pi, 3 * math.pi / 2, 10)

    speed_color = RED if speed > 105 else TEXT_COLOR
    speed_text = font_large.render(f"{int(speed)}", True, speed_color)
    screen.blit(speed_text, (speed_pos[0] - speed_text.get_width() // 2, speed_pos[1] - 20))
    kmh_text = font_small.render("km/h", True, TEXT_COLOR)
    screen.blit(kmh_text, (speed_pos[0] - kmh_text.get_width() // 2, speed_pos[1] + 40))

    # --- RPM Bar ---
    rpm_label = font_small.render("RPM", True, TEXT_COLOR)
    screen.blit(rpm_label, (WIDTH // 2 - rpm_label.get_width() // 2, 330))
    rpm_segments = 12
    segment_width = 30
    segment_spacing = 10
    bar_width = rpm_segments * segment_width + (rpm_segments - 1) * segment_spacing
    start_x = (WIDTH - bar_width) // 2
    rpm_percent = min(rpm / 6000, 1.0)

    for i in range(rpm_segments):
        if i < 7:
            color = GREEN if (i / rpm_segments) < rpm_percent else (80, 80, 80)
        elif i < 10:
            color = (255,255,0) if (i / rpm_segments) < rpm_percent else (80, 80, 80)
        else:
            color = RED if (i / rpm_segments) < rpm_percent else (80, 80, 80)
        pygame.draw.rect(screen, color, (start_x + i * (segment_width + segment_spacing), 360, segment_width, 30))

    # --- Clutch ---
    clutch_label = font_small.render("Clutch", True, TEXT_COLOR)
    screen.blit(clutch_label, (100, 420))
    clutch_text = font_small.render("Pressed" if clutch_pressed else "Released", True, RED if clutch_pressed else GREEN)
    screen.blit(clutch_text, (100, 450))

    # --- Brake ---
    brake_label = font_small.render("Brake", True, TEXT_COLOR)
    screen.blit(brake_label, (WIDTH - 250, 420))
    brake_text = font_small.render("Pressed" if brake_pressed else "Released", True, RED if brake_pressed else GREEN)
    screen.blit(brake_text, (WIDTH - 250, 450))

    # --- Buttons ---
    button_width = 200
    button_height = 50

    # CarPlay Button
    pygame.draw.rect(screen, BUTTON_COLOR, (50, 500, button_width, button_height), border_radius=10)
    apple_carplay_text = font_small.render("Apple CarPlay", True, BUTTON_TEXT_COLOR)
    carplay_rect = apple_carplay_text.get_rect(center=(50 + button_width // 2, 500 + button_height // 2))
    screen.blit(apple_carplay_text, carplay_rect)

    # Settings Button
    pygame.draw.rect(screen, BUTTON_COLOR, (WIDTH - 50 - button_width, 500, button_width, button_height), border_radius=10)
    settings_text = font_small.render("Settings", True, BUTTON_TEXT_COLOR)
    settings_rect = settings_text.get_rect(center=(WIDTH - 50 - button_width // 2, 500 + button_height // 2))
    screen.blit(settings_text, settings_rect)

    # Tools Button (top right)
    about_button_rect = pygame.Rect(WIDTH - 150, 50, 100, 30)
    pygame.draw.rect(screen, BUTTON_COLOR, about_button_rect, border_radius=5)
    tools_text = font_small.render("Tools", True, BUTTON_TEXT_COLOR)
    tools_rect = tools_text.get_rect(center=about_button_rect.center)
    screen.blit(tools_text, tools_rect)

    # --- Version ---
    version_text = font_small.render(f"Version: {settings_json['Program']['version']}", True, TEXT_COLOR)
    screen.blit(version_text, (WIDTH // 2 - version_text.get_width() // 2, HEIGHT - 25))


# Laad de afbeeldingen als textures
main_bg = pygame.image.load('images/main_bg.png').convert_alpha()
tach_8000 = pygame.image.load('images/tach_6000.png').convert_alpha()
needle_revs = pygame.image.load('images/needle_revs.png').convert_alpha()

# Laad gears
gear_textures = {
    1: pygame.image.load('images/1.png').convert_alpha(),
    2: pygame.image.load('images/2.png').convert_alpha(),
    3: pygame.image.load('images/3.png').convert_alpha(),
    4: pygame.image.load('images/4.png').convert_alpha(),
    5: pygame.image.load('images/5.png').convert_alpha(),
}

def dirt_dashboard(throttle, speed, rpm, clutch_pressed, brake_pressed, gear):
    screen.fill(BACKGROUND_COLOR)

    center_x = WIDTH // 2
    center_y = HEIGHT // 2 + 40

    # --- Tachometer Background ---
    scaled_main_bg = pygame.transform.scale(main_bg, (int(main_bg.get_width() * 1.2), int(main_bg.get_height() * 1.2)))
    main_bg_rect = scaled_main_bg.get_rect(center=(center_x, center_y - 100))
    screen.blit(scaled_main_bg, main_bg_rect)

    tach_rect = tach_8000.get_rect(center=(center_x + 5, center_y - 130))
    screen.blit(tach_8000, tach_rect)

    # --- Needle ---
    rpm_clamped = min(max(rpm, 0), 6000)
    angle_range = 240
    base_angle = -134
    needle_angle = base_angle + (rpm_clamped / 6000) * angle_range

    scaled_needle = pygame.transform.scale(needle_revs, (int(needle_revs.get_width() * 0.8), int(needle_revs.get_height() * 1.7)))
    pivot_surface = pygame.Surface((400, 400), pygame.SRCALPHA)
    pivot_x, pivot_y = 200, 200

    needle_pos = (
        pivot_x - scaled_needle.get_width() // 2,
        pivot_y - int(scaled_needle.get_height() * 0.76)
    )
    pivot_surface.blit(scaled_needle, needle_pos)

    rotated_pivot_surface = pygame.transform.rotozoom(pivot_surface, -needle_angle, 1.0)
    rotated_pivot_rect = rotated_pivot_surface.get_rect(center=(center_x + 3, center_y - 95))
    screen.blit(rotated_pivot_surface, rotated_pivot_rect)

    # --- Gear Icon ---
    if gear in gear_textures:
        gear_texture = gear_textures[gear]
        gear_rect = gear_texture.get_rect(center=(center_x - 102, center_y - 10))
        screen.blit(gear_texture, gear_rect)

    # --- Speed ---
    speed_text = font_large.render(str(int(speed)), True, (0, 0, 0))
    screen.blit(speed_text, (center_x - speed_text.get_width() // 2 + 3, center_y - 62))
    kmh_text = font_small.render("KMH", True, TEXT_COLOR)
    screen.blit(kmh_text, (center_x - kmh_text.get_width() // 2, center_y + 25))

    # --- Clutch Indicator ---
    clutch_label = font_small.render("Clutch", True, TEXT_COLOR)
    clutch_text = font_small.render("Pressed" if clutch_pressed else "Released", True, RED if clutch_pressed else GREEN)
    screen.blit(clutch_label, (60, HEIGHT - 100))
    screen.blit(clutch_text, (60, HEIGHT - 75))

    # --- Brake Indicator ---
    brake_label = font_small.render("Brake", True, TEXT_COLOR)
    brake_text = font_small.render("Pressed" if brake_pressed else "Released", True, RED if brake_pressed else GREEN)
    screen.blit(brake_label, (WIDTH - 160, HEIGHT - 100))
    screen.blit(brake_text, (WIDTH - 160, HEIGHT - 75))

    # --- Bottom Buttons ---
    button_width = 200
    button_height = 50
    button_y = HEIGHT - 100

    # CarPlay Button
    pygame.draw.rect(screen, BUTTON_COLOR, (50, button_y, button_width, button_height), border_radius=10)
    carplay_text = font_small.render("Apple CarPlay", True, BUTTON_TEXT_COLOR)
    carplay_rect = carplay_text.get_rect(center=(50 + button_width // 2, button_y + button_height // 2))
    screen.blit(carplay_text, carplay_rect)

    # Settings Button
    pygame.draw.rect(screen, BUTTON_COLOR, (WIDTH - 50 - button_width, button_y, button_width, button_height), border_radius=10)
    settings_text = font_small.render("Settings", True, BUTTON_TEXT_COLOR)
    settings_rect = settings_text.get_rect(center=(WIDTH - 50 - button_width // 2, button_y + button_height // 2))
    screen.blit(settings_text, settings_rect)

    # Tools Button (Top-right)
    tools_rect = pygame.Rect(WIDTH - 150, 50, 100, 30)
    pygame.draw.rect(screen, BUTTON_COLOR, tools_rect, border_radius=5)
    tools_text = font_small.render("Tools", True, BUTTON_TEXT_COLOR)
    text_rect = tools_text.get_rect(center=tools_rect.center)
    screen.blit(tools_text, text_rect)

    # --- Version ---
    version_text = font_small.render(f"Version: {settings_json['Program']['version']}", True, TEXT_COLOR)
    screen.blit(version_text, (WIDTH // 2 - version_text.get_width() // 2, HEIGHT - 25))


def futuristic_dashboard(throttle, speed, rpm, clutch_pressed, brake_pressed, gear):
    screen.fill(BACKGROUND_COLOR)

    # Dashboard Title
    title_surface = font_large.render("Fusion Drive", True, (0, 200, 255))
    screen.blit(title_surface, ((WIDTH - title_surface.get_width()) // 2, 20))

    # Speed - large center text
    speed_text = font_super_large.render(f"{int(speed)}", True, (0, 255, 180))
    screen.blit(speed_text, (WIDTH // 2 - speed_text.get_width() // 2, HEIGHT // 2 - 150))
    kmh_text = font_small.render("km/h", True, (150, 150, 255))
    screen.blit(kmh_text, (WIDTH // 2 - kmh_text.get_width() // 2, HEIGHT // 2 - 70))

    # Throttle bar (left side)
    bar_x = 100
    bar_y = 150
    bar_width = 30
    bar_height = 300
    filled_height = int((throttle / 100) * bar_height)

    pygame.draw.rect(screen, (50, 50, 100), (bar_x, bar_y, bar_width, bar_height))  # background
    pygame.draw.rect(screen, (0, 255, 100), (bar_x, bar_y + (bar_height - filled_height), bar_width, filled_height))  # fill

    # Throttle label (centered under bar)
    throttle_label = font_small.render("Throttle", True, (200, 200, 255))
    screen.blit(throttle_label, (bar_x + (bar_width - throttle_label.get_width()) // 2, bar_y + bar_height + 10))

    # RPM horizontal bar (bottom center)
    rpm = min(rpm, 8000)  # Clamp to max
    rpm_percent = rpm / 8000
    rpm_bar_width = int(rpm_percent * (WIDTH - 200))

    pygame.draw.rect(screen, (80, 80, 120), (100, HEIGHT - 80, WIDTH - 200, 20))  # background

    if rpm < 5000:
        rpm_color = (0, 255, 100)
    elif rpm < 7000:
        rpm_color = (255, 255, 0)
    else:
        rpm_color = (255, 50, 50)

    pygame.draw.rect(screen, rpm_color, (100, HEIGHT - 80, rpm_bar_width, 20))  # fill

    rpm_text = font_small.render(f"RPM: {int(rpm)}", True, (150, 150, 255))
    screen.blit(rpm_text, (WIDTH // 2 - rpm_text.get_width() // 2, HEIGHT - 110))

    # Gear display (right center)
    gear_label = font_large.render(str(gear) if gear != -1 else "N", True, (255, 255, 255))
    screen.blit(gear_label, (WIDTH - 150 - gear_label.get_width() // 2, HEIGHT // 2 - 100))

    # Clutch indicator (bottom left)
    clutch_text = font_small.render(f"Clutch: {'Pressed' if clutch_pressed else 'Released'}", True,
                                    (255, 100, 100) if clutch_pressed else (100, 255, 100))
    screen.blit(clutch_text, (50, HEIGHT - 50))

    # Brake indicator (bottom right)
    brake_text = font_small.render(f"Brake: {'Pressed' if brake_pressed else 'Released'}", True,
                                   (255, 100, 100) if brake_pressed else (100, 255, 100))
    screen.blit(brake_text, (WIDTH - 250, HEIGHT - 50))

    # Buttons
    button_width = 150
    button_height = 40

    # CarPlay
    pygame.draw.rect(screen, (30, 30, 80), (50, 500, button_width, button_height), border_radius=10)
    carplay_text = font_small.render("Apple CarPlay", True, (0, 255, 200))
    screen.blit(carplay_text, (
        50 + (button_width - carplay_text.get_width()) // 2,
        500 + (button_height - carplay_text.get_height()) // 2
    ))

    # Settings
    pygame.draw.rect(screen, (30, 30, 80), (WIDTH - 50 - button_width, 500, button_width, button_height), border_radius=10)
    settings_text = font_small.render("Settings", True, (0, 255, 200))
    screen.blit(settings_text, (
        WIDTH - 50 - button_width + (button_width - settings_text.get_width()) // 2,
        500 + (button_height - settings_text.get_height()) // 2
    ))

    # Tools button (top right)
    about_button_rect = pygame.Rect(WIDTH - 150, 50, 100, 30)
    pygame.draw.rect(screen, (30, 30, 80), about_button_rect, border_radius=5)
    tools_text = font_small.render("Tools", True, (0, 255, 200))
    text_rect = tools_text.get_rect(center=about_button_rect.center)
    screen.blit(tools_text, text_rect)

    # Version
    version_text = font_small.render(f"Version: {settings_json['Program']['version']}", True, (100, 100, 150))
    screen.blit(version_text, (WIDTH // 2 - version_text.get_width() // 2, HEIGHT - 40))

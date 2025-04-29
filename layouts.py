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
    screen.fill((20, 20, 25))  # Darker background

    # Title (centered)
    title_surface = font_large.render("Ford Fiesta MK6 Sport", True, TEXT_COLOR)
    screen.blit(title_surface, ((WIDTH - title_surface.get_width()) // 2, 30))

    # Circle positions
    throttle_pos = (250, 180)
    speed_pos = (WIDTH - 250, 180)

    # Draw Throttle Circle
    pygame.draw.circle(screen, (60, 60, 70), throttle_pos, 100)
    pygame.draw.arc(screen, BLUE, (throttle_pos[0] - 100, throttle_pos[1] - 100, 200, 200),
                    3 * math.pi / 2 - (throttle / 100) * 2 * math.pi, 3 * math.pi / 2, 10)
    throttle_text = font_large.render(f"{throttle}%", True, TEXT_COLOR)
    screen.blit(throttle_text, (throttle_pos[0] - throttle_text.get_width() // 2, throttle_pos[1] - 20))
    throttle_label = font_small.render("Throttle", True, TEXT_COLOR)
    screen.blit(throttle_label, (throttle_pos[0] - throttle_label.get_width() // 2, throttle_pos[1] + 40))

    # Draw current gear
    rpm_label = font_super_large.render(str(gear) if gear != -1 else "N", True, TEXT_COLOR)
    screen.blit(rpm_label, (WIDTH // 2 - rpm_label.get_width() // 2, 170))

    # Draw Speed Circle
    pygame.draw.circle(screen, (60, 60, 70), speed_pos, 100)
    arc_color = RED if speed > 105 else GREEN
    pygame.draw.arc(screen, arc_color, (speed_pos[0] - 100, speed_pos[1] - 100, 200, 200),
                    3 * math.pi / 2 - (speed / 200) * 2 * math.pi, 3 * math.pi / 2, 10)
    speed_text = font_large.render(f"{int(speed)}", True, TEXT_COLOR)
    screen.blit(speed_text, (speed_pos[0] - speed_text.get_width() // 2, speed_pos[1] - 20))
    kmh_text = font_small.render("km/h", True, TEXT_COLOR)
    screen.blit(kmh_text, (speed_pos[0] - kmh_text.get_width() // 2, speed_pos[1] + 40))

    # RPM Bar (centered below circles)
    rpm_label = font_small.render("RPM", True, TEXT_COLOR)
    screen.blit(rpm_label, (WIDTH // 2 - rpm_label.get_width() // 2, 330))
    rpm_segments = 10
    segment_width = 30
    segment_spacing = 10
    bar_width = rpm_segments * segment_width + (rpm_segments - 1) * segment_spacing
    start_x = (WIDTH - bar_width) // 2
    rpm_percent = min(rpm / 6000, 1.0)

    for i in range(rpm_segments):
        color = RED if (i / rpm_segments) < rpm_percent else (80, 80, 80)
        pygame.draw.rect(screen, color, (start_x + i * (segment_width + segment_spacing), 360, segment_width, 30))

    # Clutch
    clutch_label = font_small.render("Clutch", True, TEXT_COLOR)
    screen.blit(clutch_label, (100, 420))
    clutch_text = font_small.render("Pressed" if clutch_pressed else "Released", True, RED if clutch_pressed else GREEN)
    screen.blit(clutch_text, (100, 450))

    # Brake
    brake_label = font_small.render("Brake", True, TEXT_COLOR)
    screen.blit(brake_label, (WIDTH - 250, 420))
    brake_text = font_small.render("Pressed" if brake_pressed else "Released", True, RED if brake_pressed else GREEN)
    screen.blit(brake_text, (WIDTH - 250, 450))

    # Bottom Buttons (CarPlay, Misc, Settings)
    button_width = 200
    button_height = 50
    spacing = 40

    # Carplay
    pygame.draw.rect(screen, BUTTON_COLOR, (50, 500, button_width, button_height))
    apple_carplay_text = font_small.render("Apple CarPlay", True, BUTTON_TEXT_COLOR)
    text_rect = apple_carplay_text.get_rect(center=(50 + button_width // 2, 500 + button_height // 2))
    screen.blit(apple_carplay_text, text_rect)

    about_button_rect = pygame.Rect(WIDTH - 150, 50, 100, 30)
    pygame.draw.rect(screen, BUTTON_COLOR, about_button_rect)
    tools_text = font_small.render("Tools", True, BUTTON_TEXT_COLOR)
    text_rect = tools_text.get_rect(center=about_button_rect.center)
    screen.blit(tools_text, text_rect)

    # Settings Button
    pygame.draw.rect(screen, BUTTON_COLOR, (WIDTH - 50 - button_width, 500, button_width, button_height))
    settings_text = font_small.render("Settings", True, BUTTON_TEXT_COLOR)
    text_rect = settings_text.get_rect(center=(WIDTH - 50 - button_width // 2, 500 + button_height // 2))
    screen.blit(settings_text, text_rect)

    # Version
    version_text = font_small.render(f"Version: {settings_json['Program']['version']}", True, TEXT_COLOR)
    screen.blit(version_text, (WIDTH // 2 - version_text.get_width() // 2, HEIGHT - 25))

# Laad de afbeeldingen als textures
main_bg = pygame.image.load('images/main_bg.png').convert_alpha()
tach_8000 = pygame.image.load('images/tach_8000.png').convert_alpha()
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
    screen.fill((20, 20, 25))

    # Center van het scherm (iets naar beneden)
    center_x = WIDTH // 2
    center_y = HEIGHT // 2 + 40

    # Main background bevat al RPM schaal
    scaled_main_bg = pygame.transform.scale(main_bg, (int(main_bg.get_width() * 1.2), int(main_bg.get_height() * 1.2)))
    main_bg_rect = scaled_main_bg.get_rect(center=(center_x, center_y - 100))
    screen.blit(scaled_main_bg, main_bg_rect)

    tach_rect = tach_8000.get_rect(center=(center_x + 5, center_y - 130))
    screen.blit(tach_8000, tach_rect)

    # Needle (draait bovenop main_bg)
    rpm_clamped = min(max(rpm, 0), 8000)
    angle_range = 229  # totaal bereik
    base_angle = -120  # start aan linkerkant
    needle_angle = base_angle + (rpm_clamped / 8000) * angle_range

    # Scale needle
    scaled_needle = pygame.transform.scale(needle_revs, (int(needle_revs.get_width() * 0.8), int(needle_revs.get_height() * 1.7)))

    # Maak een grotere surface voor de needle
    pivot_surface_size = (400, 400)  # Groot genoeg zodat alles past
    pivot_surface = pygame.Surface(pivot_surface_size, pygame.SRCALPHA)

    # Plaats de needle op de pivot_surface zodat de basis van de needle (bijv. 85% van de hoogte) op het center komt
    pivot_x = pivot_surface_size[0] // 2
    pivot_y = pivot_surface_size[1] // 2

    needle_pos = (
        pivot_x - scaled_needle.get_width() // 2,
        pivot_y - int(scaled_needle.get_height() * 0.76)
    )
    pivot_surface.blit(scaled_needle, needle_pos)

    # Roteer de volledige pivot surface
    rotated_pivot_surface = pygame.transform.rotozoom(pivot_surface, -needle_angle, 1.0)
    rotated_pivot_rect = rotated_pivot_surface.get_rect(center=(center_x + 2, center_y - 90))

    # Teken het resultaat
    screen.blit(rotated_pivot_surface, rotated_pivot_rect)


    # Gear icoon (net onder de wijzer)
    if gear in gear_textures:
        gear_texture = gear_textures[gear]
        gear_rect = gear_texture.get_rect(center=(center_x - 102, center_y - 10))
        screen.blit(gear_texture, gear_rect)

    # Snelheid in het midden van de tacho
    speed_text = font_large.render(str(int(speed)), True, (0, 0, 0))
    screen.blit(speed_text, (center_x - speed_text.get_width() // 2, center_y - 50))
    kmh_text = font_small.render("KMH", True, TEXT_COLOR)
    screen.blit(kmh_text, (center_x - kmh_text.get_width() // 2, center_y + 25))

    # Clutch indicator (linksonder)
    clutch_label = font_small.render("Clutch", True, TEXT_COLOR)
    screen.blit(clutch_label, (50, HEIGHT - 100))
    clutch_text = font_small.render("Pressed" if clutch_pressed else "Released", True, RED if clutch_pressed else GREEN)
    screen.blit(clutch_text, (50, HEIGHT - 70))

    # Brake indicator (rechtsonder)
    brake_label = font_small.render("Brake", True, TEXT_COLOR)
    screen.blit(brake_label, (WIDTH - 150, HEIGHT - 100))
    brake_text = font_small.render("Pressed" if brake_pressed else "Released", True, RED if brake_pressed else GREEN)
    screen.blit(brake_text, (WIDTH - 150, HEIGHT - 70))

        # Bottom Buttons (CarPlay, Tools, Settings)
    button_width = 200
    button_height = 50

    # CarPlay knop
    pygame.draw.rect(screen, BUTTON_COLOR, (50, 500, button_width, button_height))
    apple_carplay_text = font_small.render("Apple CarPlay", True, BUTTON_TEXT_COLOR)
    text_rect = apple_carplay_text.get_rect(center=(50 + button_width // 2, 500 + button_height // 2))
    screen.blit(apple_carplay_text, text_rect)

    # Settings knop
    pygame.draw.rect(screen, BUTTON_COLOR, (WIDTH - 50 - button_width, 500, button_width, button_height))
    settings_text = font_small.render("Settings", True, BUTTON_TEXT_COLOR)
    text_rect = settings_text.get_rect(center=(WIDTH - 50 - button_width // 2, 500 + button_height // 2))
    screen.blit(settings_text, text_rect)

    # Tools knop (rechtsboven)
    about_button_rect = pygame.Rect(WIDTH - 150, 50, 100, 30)
    pygame.draw.rect(screen, BUTTON_COLOR, about_button_rect)
    tools_text = font_small.render("Tools", True, BUTTON_TEXT_COLOR)
    text_rect = tools_text.get_rect(center=about_button_rect.center)
    screen.blit(tools_text, text_rect)


    # Version label onderin
    version_text = font_small.render(f"Version: {settings_json['Program']['version']}", True, TEXT_COLOR)
    screen.blit(version_text, (WIDTH // 2 - version_text.get_width() // 2, HEIGHT - 25))

def f1_dashboard(throttle, speed, rpm, clutch_pressed, brake_pressed, gear):
    screen.fill((10, 10, 15))  # Donkere cockpit-achtergrond

    center_x = WIDTH // 2
    center_y = HEIGHT // 2

    # RPM LED-balk bovenin
    rpm_percent = min(rpm / 12000, 1.0)  # 12000 RPM als max
    led_count = 15
    active_leds = int(led_count * rpm_percent)
    led_width = 20
    led_height = 10
    spacing = 5
    start_x = center_x - (led_count * (led_width + spacing)) // 2

    for i in range(led_count):
        if i < active_leds:
            color = (255, 0, 0) if i > 10 else (255, 255, 0) if i > 5 else (0, 255, 0)
        else:
            color = (30, 30, 30)  # Uit LED

        led_rect = pygame.Rect(start_x + i * (led_width + spacing), 100, led_width, led_height)
        pygame.draw.rect(screen, color, led_rect)

    # Gear groot in het midden
    gear_text = font_large.render(str(gear), True, TEXT_COLOR)
    screen.blit(gear_text, (center_x - gear_text.get_width() // 2, center_y - 40))

    # Speed onder gear
    speed_text = font_small.render(f"{int(speed)} KM/H", True, TEXT_COLOR)
    screen.blit(speed_text, (center_x - speed_text.get_width() // 2, center_y + 40))

    # Clutch indicator (linksonder)
    clutch_label = font_small.render("Clutch", True, TEXT_COLOR)
    screen.blit(clutch_label, (50, HEIGHT - 100))
    clutch_text = font_small.render("Pressed" if clutch_pressed else "Released", True, (255, 0, 0) if clutch_pressed else (0, 255, 0))
    screen.blit(clutch_text, (50, HEIGHT - 70))

    # Brake indicator (rechtsonder)
    brake_label = font_small.render("Brake", True, TEXT_COLOR)
    screen.blit(brake_label, (WIDTH - 150, HEIGHT - 100))
    brake_text = font_small.render("Pressed" if brake_pressed else "Released", True, (255, 0, 0) if brake_pressed else (0, 255, 0))
    screen.blit(brake_text, (WIDTH - 150, HEIGHT - 70))

        # Bottom Buttons (CarPlay, Tools, Settings)
    button_width = 200
    button_height = 50

    # CarPlay knop
    pygame.draw.rect(screen, BUTTON_COLOR, (50, 500, button_width, button_height))
    apple_carplay_text = font_small.render("Apple CarPlay", True, BUTTON_TEXT_COLOR)
    text_rect = apple_carplay_text.get_rect(center=(50 + button_width // 2, 500 + button_height // 2))
    screen.blit(apple_carplay_text, text_rect)

    # Settings knop
    pygame.draw.rect(screen, BUTTON_COLOR, (WIDTH - 50 - button_width, 500, button_width, button_height))
    settings_text = font_small.render("Settings", True, BUTTON_TEXT_COLOR)
    text_rect = settings_text.get_rect(center=(WIDTH - 50 - button_width // 2, 500 + button_height // 2))
    screen.blit(settings_text, text_rect)

    # Tools knop (rechtsboven)
    about_button_rect = pygame.Rect(WIDTH - 150, 50, 100, 30)
    pygame.draw.rect(screen, BUTTON_COLOR, about_button_rect)
    tools_text = font_small.render("Tools", True, BUTTON_TEXT_COLOR)
    text_rect = tools_text.get_rect(center=about_button_rect.center)
    screen.blit(tools_text, text_rect)


    # Version onderaan
    version_text = font_small.render(f"Version: {settings_json['Program']['version']}", True, TEXT_COLOR)
    screen.blit(version_text, (WIDTH // 2 - version_text.get_width() // 2, HEIGHT - 25))

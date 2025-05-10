import pygame
import math
from Carviewer_dummy import *


# Function to draw dashboard
def original_dashboard(throttle, speed, rpm, clutch_pressed, brake_pressed, gear):
    screen.fill(BACKGROUND_COLOR)
    
    # Title
    title_text = font_large.render("Ford Fiesta MK6 Sport", True, TEXT_COLOR)
    screen.blit(title_text, (50, 50))
    
    # About Button
    about_button_rect = pygame.Rect(WIDTH - 150, 50, 100, 30, border_radius=10)
    pygame.draw.rect(screen, BUTTON_COLOR, about_button_rect)
    tools_text = font_small.render("Tools", True, BUTTON_TEXT_COLOR)
    text_rect = tools_text.get_rect(center=about_button_rect.center)
    screen.blit(tools_text, text_rect)

    # version label
    version_text = font_small.render(f"Version: {settings_json['Program']['version']}", True, TEXT_COLOR)
    
    screen.blit(version_text, (WIDTH // 2 - version_text.get_width() // 2, 526))
    
    # Throttle
    throttle_label = font_small.render("RPM", True, TEXT_COLOR)
    screen.blit(throttle_label, (50, 150))
    # pygame.draw.rect(screen, BUTTON_COLOR, (250, 150, throttle * 2, 30))

    # --- Gear ---
    rpm_label = font_super_large.render(str(gear) if gear != -1 else "N", True, TEXT_COLOR if rpm < 4500 else RED)
    screen.blit(rpm_label, (WIDTH // 2 - rpm_label.get_width() // 2, 475))

    throttle_circle_radius = 100
    pygame.draw.circle(screen, TEXT_COLOR, (300, 200), throttle_circle_radius, 3)
    pygame.draw.arc(screen, TEXT_COLOR, (200, 100, 200, 200), 3 * math.pi / 2 - (rpm / 6000) * 2 * math.pi, 3 * math.pi / 2, 10)


    throttle_text = font_large.render(str(rpm), True, TEXT_COLOR)
    screen.blit(throttle_text, (300 - throttle_text.get_width() / 2, 200 - throttle_text.get_height() / 2))
    # percent_text = font_small.render("%", True, TEXT_COLOR)
    # screen.blit(percent_text, (325, 190))
    
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

    # # RPM test
    # rpm_label = font_small.render("RPM", True, TEXT_COLOR)
    # screen.blit(rpm_label, (420, 475))
    # rpm_text = font_small.render(str(rpm), True, RED if rpm > 4500 else TEXT_COLOR)
    # screen.blit(rpm_text, (550, 475))
    
    # Draw horizontal lines
    pygame.draw.line(screen, TEXT_COLOR, (50, 330), (950, 330), 2)
    pygame.draw.line(screen, TEXT_COLOR, (50, 450), (950, 450), 2)
    
    # Draw buttons
    button_width = 200
    button_height = 50
    
    pygame.draw.rect(screen, BUTTON_COLOR, (50, 500, button_width, button_height), border_radius=10)
    apple_carplay_text = font_small.render("Apple CarPlay", True, BUTTON_TEXT_COLOR)
    text_rect = apple_carplay_text.get_rect(center=(50 + button_width // 2, 500 + button_height // 2))
    screen.blit(apple_carplay_text, text_rect)
    
    pygame.draw.rect(screen, BUTTON_COLOR, (WIDTH - 50 - button_width, 500, button_width, button_height), border_radius=10)
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
    rpm_label = font_super_large.render(str(gear) if gear != -1 else "N", True, TEXT_COLOR if rpm < 4500 else RED)
    screen.blit(rpm_label, (WIDTH // 2 - rpm_label.get_width() // 2, 200))

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
    screen.blit(version_text, (WIDTH // 2 - version_text.get_width() // 2, HEIGHT - 50))


# Laad de afbeeldingen als textures
main_bg = pygame.image.load('images/main_bg.png').convert_alpha()
dirt2 = pygame.image.load('images/dirt2.png').convert_alpha()
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

    main_bg_y_offset = -50

    # --- DiRT 2 logo ---
    scaled_dirt2 = pygame.transform.scale(dirt2, (int(dirt2.get_width()*0.6), int(dirt2.get_height()*0.6)))
    dirt2_rect = scaled_dirt2.get_rect(center=(center_x - 325, center_y - 225))
    screen.blit(scaled_dirt2, dirt2_rect)

    # --- Tachometer Background ---
    scaled_main_bg = pygame.transform.scale(main_bg, (int(main_bg.get_width() * 1.2), int(main_bg.get_height() * 1.2)))
    main_bg_rect = scaled_main_bg.get_rect(center=(center_x, center_y + main_bg_y_offset))
    screen.blit(scaled_main_bg, main_bg_rect)

    tach_rect = tach_8000.get_rect(center=(center_x + 5, center_y + main_bg_y_offset - 30))
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
    rotated_pivot_rect = rotated_pivot_surface.get_rect(center=(center_x + 3, center_y + main_bg_y_offset + 5))
    screen.blit(rotated_pivot_surface, rotated_pivot_rect)

    # --- Gear Icon ---
    if gear in gear_textures:
        gear_texture = gear_textures[gear]
        gear_rect = gear_texture.get_rect(center=(center_x - 102, center_y + main_bg_y_offset + 90))
        screen.blit(gear_texture, gear_rect)

    # --- Speed ---
    speed_text = font_large.render(str(int(speed)), True, (0, 0, 0))
    screen.blit(speed_text, (center_x - speed_text.get_width() // 2 + 3, center_y + main_bg_y_offset + 38))
    kmh_text = font_small.render("KMH", True, TEXT_COLOR)
    screen.blit(kmh_text, (center_x - kmh_text.get_width() // 2, center_y + main_bg_y_offset + 125))

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
    screen.blit(version_text, (WIDTH // 2 - version_text.get_width() // 2, HEIGHT - 50))


def modern_dashboard(throttle, speed, rpm, clutch_pressed, brake_pressed, gear):
    screen.fill(BACKGROUND_COLOR)

    # --- Top HUD Bar ---
    title = font_large.render("Ford Fiesta MK6 Sport", True, TEXT_COLOR)
    screen.blit(title, (40, 20))

    tools_button = pygame.Rect(864, 20, 120, 30)
    pygame.draw.rect(screen, BUTTON_COLOR, tools_button, border_radius=10)
    tools_text = font_small.render("Tools", True, BUTTON_TEXT_COLOR)
    screen.blit(tools_text, tools_text.get_rect(center=tools_button.center))

    # --- RPM Bar (Left Section) ---
    rpm_label = font_small.render("Engine RPM", True, TEXT_COLOR)
    screen.blit(rpm_label, (40, 100))

    rpm_bar_x = 40
    rpm_bar_y = 135
    rpm_bar_width = 360
    rpm_bar_height = 30
    rpm_ratio = min(rpm / 6000, 1.0)

    pygame.draw.rect(screen, TEXT_COLOR, (rpm_bar_x, rpm_bar_y, rpm_bar_width, rpm_bar_height), 2)
    pygame.draw.rect(screen, GREEN if rpm < 4500 else RED,
                     (rpm_bar_x, rpm_bar_y, rpm_bar_width * rpm_ratio, rpm_bar_height))

    rpm_text = font_large.render(f"{rpm} RPM", True, TEXT_COLOR)
    screen.blit(rpm_text, (rpm_bar_x, rpm_bar_y + 40))

    # --- Speed and Gear (Center) ---
    gear_str = str(gear) if gear != -1 else "N"
    gear_text = font_large.render(f"Gear: {gear_str}", True, TEXT_COLOR)
    screen.blit(gear_text, (460, 130))

    speed_text = font_super_large.render(str(int(speed)), True, RED if speed > 105 else TEXT_COLOR)
    speed_label = font_large.render("km/h", True, TEXT_COLOR)
    screen.blit(speed_text, (512 - speed_text.get_width() // 2, 200))
    screen.blit(speed_label, (512 - speed_label.get_width() // 2, 275))

    # --- Indicators (Right Side) ---
    indicator_x = 700
    indicator_y = 130

    clutch_box = pygame.Rect(indicator_x, indicator_y, 260, 55)
    pygame.draw.rect(screen, RED if clutch_pressed else GREEN, clutch_box, border_radius=8)
    clutch_text = font_small.render(f"🦶 Clutch: {'Pressed' if clutch_pressed else 'Released'}", True, BUTTON_TEXT_COLOR)
    screen.blit(clutch_text, clutch_text.get_rect(center=clutch_box.center))

    brake_box = pygame.Rect(indicator_x, indicator_y + 80, 260, 55)
    pygame.draw.rect(screen, RED if brake_pressed else GREEN, brake_box, border_radius=8)
    brake_text = font_small.render(f"🛑 Brake: {'Pressed' if brake_pressed else 'Released'}", True, BUTTON_TEXT_COLOR)
    screen.blit(brake_text, brake_text.get_rect(center=brake_box.center))

    # --- Bottom Controls (spaced further down) ---
    # Apple CarPlay
    pygame.draw.rect(screen, BUTTON_COLOR, (100, 500, 200, 55), border_radius=10)
    carplay_text = font_small.render("Apple CarPlay", True, BUTTON_TEXT_COLOR)
    screen.blit(carplay_text, carplay_text.get_rect(center=(200, 527)))

    # Settings
    pygame.draw.rect(screen, BUTTON_COLOR, (724, 500, 200, 55), border_radius=10)
    settings_text = font_small.render("Settings", True, BUTTON_TEXT_COLOR)
    screen.blit(settings_text, settings_text.get_rect(center=(824, 527)))

    # --- Version Info (bottom center) ---
    version_text = font_small.render(f"Version: {settings_json['Program']['version']}", True, TEXT_COLOR)
    screen.blit(version_text, (512 - version_text.get_width() // 2, 560))

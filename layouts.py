import pygame
import math
from Carviewer_Arduino import *
import cruise

def draw_cruise_set(center, font=None):
    # Cruise control target speed in green, only while cruise control is enabled
    if not cruise.enabled:
        return
    text = (font or font_small).render(str(int(cruise.desiredSpeed)), True, GREEN)
    screen.blit(text, text.get_rect(center=center))

# Function to draw dashboard
def original_dashboard(throttle, speed, rpm, clutch_pressed, brake_pressed, gear):
    screen.fill(BACKGROUND_COLOR)
    
    # Title
    title_text = font_large.render("Ford Fiesta MK6 Sport", True, TEXT_COLOR)
    screen.blit(title_text, (S(50), S(50)))
    
    # About Button
    about_button_rect = pygame.Rect(WIDTH - S(150), S(50), S(100), S(30), border_radius=S(10))
    pygame.draw.rect(screen, BUTTON_COLOR, about_button_rect)
    tools_text = font_small.render("Tools", True, BUTTON_TEXT_COLOR)
    text_rect = tools_text.get_rect(center=about_button_rect.center)
    screen.blit(tools_text, text_rect)

    # version label
    version_text = font_small.render(f"Version: {settings_json['Program']['version']}", True, TEXT_COLOR)
    
    screen.blit(version_text, (WIDTH // 2 - version_text.get_width() // 2, S(526)))
    
    # Throttle
    throttle_label = font_small.render("RPM", True, TEXT_COLOR)
    screen.blit(throttle_label, (S(50), S(150)))
    # pygame.draw.rect(screen, BUTTON_COLOR, (S(250), S(150), throttle * 2, S(30)))

    # --- Gear ---
    rpm_label = font_super_large.render(str(gear) if gear != -1 else "N", True, TEXT_COLOR if rpm < 4500 else RED)
    screen.blit(rpm_label, (WIDTH // 2 - rpm_label.get_width() // 2, S(475)))

    rpm_circle_radius = S(100)
    pygame.draw.circle(screen, TEXT_COLOR, (S(300), S(200)), rpm_circle_radius, S(3))
    pygame.draw.arc(screen, TEXT_COLOR, (S(200), S(100), S(200), S(200)), 3 * math.pi / 2 - (rpm / 6000) * 2 * math.pi, 3 * math.pi / 2, S(10))


    throttle_text = font_large.render(str(rpm), True, TEXT_COLOR)
    screen.blit(throttle_text, (S(300) - throttle_text.get_width() / 2, S(200) - throttle_text.get_height() / 2))
    # percent_text = font_small.render("%", True, TEXT_COLOR)
    # screen.blit(percent_text, (S(325), S(190)))
    
    # Speed
    speed_label = font_small.render("Speed", True, TEXT_COLOR)
    screen.blit(speed_label, (S(550), S(150)))
    
    # Draw speed circle
    speed_circle_radius = S(100)
    pygame.draw.circle(screen, TEXT_COLOR, (S(800), S(200)), speed_circle_radius, S(3))
    

    speed_text = None

    if speed > 120:
        speed_text = font_large.render(str(int(speed)), True, RED)
        pygame.draw.arc(screen, RED, (S(700), S(100), S(200), S(200)), 3 * math.pi / 2 - (speed / 200) * 2 * math.pi, 3 * math.pi / 2, S(10))
    else:
        speed_text = font_large.render(str(int(speed)), True, TEXT_COLOR)
        pygame.draw.arc(screen, TEXT_COLOR, (S(700), S(100), S(200), S(200)), 3 * math.pi / 2 - (speed / 200) * 2 * math.pi, 3 * math.pi / 2, S(10))
    
    screen.blit(speed_text, (S(800) - speed_text.get_width() / 2, S(200) - speed_text.get_height() / 2))
    kmh_text = font_small.render("km/h", True, TEXT_COLOR)
    screen.blit(kmh_text, (S(775), S(225)))
    
    # Clutch
    clutch_label = font_small.render("Clutch", True, TEXT_COLOR)
    screen.blit(clutch_label, (S(50), S(375)))
    clutch_text = font_small.render("Pressed" if clutch_pressed else "Released", True, RED if clutch_pressed else GREEN)
    screen.blit(clutch_text, (S(300), S(375)))
    
    # Brake
    brake_label = font_small.render("Brake", True, TEXT_COLOR)
    screen.blit(brake_label, (S(550), S(375)))
    brake_text = font_small.render("Pressed" if brake_pressed else "Released", True, RED if brake_pressed else GREEN)
    screen.blit(brake_text, (S(800), S(375)))
    
    # Draw horizontal lines
    pygame.draw.line(screen, TEXT_COLOR, (S(50), S(330)), (S(950), S(330)), S(2))
    pygame.draw.line(screen, TEXT_COLOR, (S(50), S(450)), (S(950), S(450)), S(2))
    
    # Draw buttons
    button_width = S(200)
    button_height = S(50)
    
    pygame.draw.rect(screen, BUTTON_COLOR, (S(50), S(500), button_width, button_height), border_radius=S(10))
    apple_carplay_text = font_small.render("Apple CarPlay", True, BUTTON_TEXT_COLOR)
    text_rect = apple_carplay_text.get_rect(center=(S(50) + button_width // 2, S(500) + button_height // 2))
    screen.blit(apple_carplay_text, text_rect)
    
    pygame.draw.rect(screen, BUTTON_COLOR, (WIDTH - S(50) - button_width, S(500), button_width, button_height), border_radius=S(10))
    settings_text = font_small.render("Settings", True, BUTTON_TEXT_COLOR)
    text_rect = settings_text.get_rect(center=(WIDTH - S(50) - button_width // 2, S(500) + button_height // 2))
    screen.blit(settings_text, text_rect)

    draw_cruise_set((S(800), S(150)))

def fancy_dashboard(throttle, speed, rpm, clutch_pressed, brake_pressed, gear):
    screen.fill(BACKGROUND_COLOR)

    # Title (centered)
    title_surface = font_large.render("Ford Fiesta MK6 Sport", True, TEXT_COLOR)
    screen.blit(title_surface, ((WIDTH - title_surface.get_width()) // 2, S(30)))

    # Circle positions
    throttle_pos = (S(250), S(180))
    speed_pos = (WIDTH - S(250), S(180))

    # --- Throttle Circle ---
    pygame.draw.circle(screen, (60, 60, 70), throttle_pos, S(100))
    pygame.draw.arc(screen, BLUE, (throttle_pos[0] - S(100), throttle_pos[1] - S(100), S(200), S(200)),
                    3 * math.pi / 2 - (throttle / 100) * 2 * math.pi, 3 * math.pi / 2, S(10))
    throttle_text = font_large.render(f"{throttle}%", True, TEXT_COLOR)
    screen.blit(throttle_text, (throttle_pos[0] - throttle_text.get_width() // 2, throttle_pos[1] - S(20)))
    throttle_label = font_small.render("Throttle", True, TEXT_COLOR)
    screen.blit(throttle_label, (throttle_pos[0] - throttle_label.get_width() // 2, throttle_pos[1] + S(40)))

    # --- Gear ---
    rpm_label = font_super_large.render(str(gear) if gear != -1 else "N", True, TEXT_COLOR if rpm < 4500 else RED)
    screen.blit(rpm_label, (WIDTH // 2 - rpm_label.get_width() // 2, S(200)))

    # --- Speed Circle ---
    pygame.draw.circle(screen, (60, 60, 70), speed_pos, S(100))
    pygame.draw.arc(screen, RED, (speed_pos[0] - S(100), speed_pos[1] - S(100), S(200), S(200)),
                    3 * math.pi / 2 - (speed / 200) * 2 * math.pi, 3 * math.pi / 2, S(10))

    speed_color = RED if speed > 120 else TEXT_COLOR
    speed_text = font_large.render(f"{int(speed)}", True, speed_color)
    screen.blit(speed_text, (speed_pos[0] - speed_text.get_width() // 2, speed_pos[1] - S(20)))
    kmh_text = font_small.render("km/h", True, TEXT_COLOR)
    screen.blit(kmh_text, (speed_pos[0] - kmh_text.get_width() // 2, speed_pos[1] + S(40)))

    # --- RPM Bar ---
    rpm_label = font_small.render("RPM", True, TEXT_COLOR)
    screen.blit(rpm_label, (WIDTH // 2 - rpm_label.get_width() // 2, S(330)))
    rpm_segments = 12
    segment_width = S(30)
    segment_spacing = S(10)
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
        pygame.draw.rect(screen, color, (start_x + i * (segment_width + segment_spacing), S(360), segment_width, S(30)))

    # --- Clutch ---
    clutch_label = font_small.render("Clutch", True, TEXT_COLOR)
    screen.blit(clutch_label, (S(100), S(420)))
    clutch_text = font_small.render("Pressed" if clutch_pressed else "Released", True, RED if clutch_pressed else GREEN)
    screen.blit(clutch_text, (S(100), S(450)))

    # --- Brake ---
    brake_label = font_small.render("Brake", True, TEXT_COLOR)
    screen.blit(brake_label, (WIDTH - S(250), S(420)))
    brake_text = font_small.render("Pressed" if brake_pressed else "Released", True, RED if brake_pressed else GREEN)
    screen.blit(brake_text, (WIDTH - S(250), S(450)))

    # --- Buttons ---
    button_width = S(200)
    button_height = S(50)

    # CarPlay Button
    pygame.draw.rect(screen, BUTTON_COLOR, (S(50), S(500), button_width, button_height), border_radius=S(10))
    apple_carplay_text = font_small.render("Apple CarPlay", True, BUTTON_TEXT_COLOR)
    carplay_rect = apple_carplay_text.get_rect(center=(S(50) + button_width // 2, S(500) + button_height // 2))
    screen.blit(apple_carplay_text, carplay_rect)

    # Settings Button
    pygame.draw.rect(screen, BUTTON_COLOR, (WIDTH - S(50) - button_width, S(500), button_width, button_height), border_radius=S(10))
    settings_text = font_small.render("Settings", True, BUTTON_TEXT_COLOR)
    settings_rect = settings_text.get_rect(center=(WIDTH - S(50) - button_width // 2, S(500) + button_height // 2))
    screen.blit(settings_text, settings_rect)

    # Tools Button (top right)
    about_button_rect = pygame.Rect(WIDTH - S(150), S(50), S(100), S(30))
    pygame.draw.rect(screen, BUTTON_COLOR, about_button_rect, border_radius=S(5))
    tools_text = font_small.render("Tools", True, BUTTON_TEXT_COLOR)
    tools_rect = tools_text.get_rect(center=about_button_rect.center)
    screen.blit(tools_text, tools_rect)

    draw_cruise_set((speed_pos[0], speed_pos[1] - S(52)))

    # --- Version ---
    version_text = font_small.render(f"Version: {settings_json['Program']['version']}", True, TEXT_COLOR)
    screen.blit(version_text, (WIDTH // 2 - version_text.get_width() // 2, HEIGHT - S(50)))


# Laad de afbeeldingen als textures (scaled to the real screen once, at load)
def _load_texture(path, scale_x=1.0, scale_y=None):
    if scale_y is None:
        scale_y = scale_x
    image = pygame.image.load(path).convert_alpha()
    return pygame.transform.scale(image, (int(image.get_width() * scale_x * SCALE), int(image.get_height() * scale_y * SCALE)))

main_bg = _load_texture('images/main_bg.png', 1.2)
dirt2 = _load_texture('images/dirt2.png', 0.6)
tach_8000 = _load_texture('images/tach_6000.png')
needle_revs = _load_texture('images/needle_revs.png', 0.8, 1.7)

# Laad gears
gear_textures = {
    1: _load_texture('images/1.png'),
    2: _load_texture('images/2.png'),
    3: _load_texture('images/3.png'),
    4: _load_texture('images/4.png'),
    5: _load_texture('images/5.png'),
}

def dirt_dashboard(throttle, speed, rpm, clutch_pressed, brake_pressed, gear):
    screen.fill(BACKGROUND_COLOR)

    center_x = WIDTH // 2
    center_y = HEIGHT // 2 + S(40)

    main_bg_y_offset = S(-50)

    # --- DiRT 2 logo ---
    dirt2_rect = dirt2.get_rect(center=(center_x - S(325), center_y - S(225)))
    screen.blit(dirt2, dirt2_rect)

    # --- Tachometer Background ---
    main_bg_rect = main_bg.get_rect(center=(center_x, center_y + main_bg_y_offset))
    screen.blit(main_bg, main_bg_rect)

    tach_rect = tach_8000.get_rect(center=(center_x + S(5), center_y + main_bg_y_offset - S(30)))
    screen.blit(tach_8000, tach_rect)

    # --- Needle ---
    rpm_clamped = min(max(rpm, 0), 6000)
    angle_range = 240
    base_angle = -134
    needle_angle = base_angle + (rpm_clamped / 6000) * angle_range

    pivot_surface = pygame.Surface((S(400), S(400)), pygame.SRCALPHA)
    pivot_x, pivot_y = S(200), S(200)

    needle_pos = (
        pivot_x - needle_revs.get_width() // 2,
        pivot_y - int(needle_revs.get_height() * 0.76)
    )
    pivot_surface.blit(needle_revs, needle_pos)

    rotated_pivot_surface = pygame.transform.rotozoom(pivot_surface, -needle_angle, 1.0)
    rotated_pivot_rect = rotated_pivot_surface.get_rect(center=(center_x + S(3), center_y + main_bg_y_offset + S(5)))
    screen.blit(rotated_pivot_surface, rotated_pivot_rect)

    # --- Gear Icon ---
    if gear in gear_textures:
        gear_texture = gear_textures[gear]
        gear_rect = gear_texture.get_rect(center=(center_x - S(102), center_y + main_bg_y_offset + S(90)))
        screen.blit(gear_texture, gear_rect)

    # --- Speed ---
    speed_text = font_large.render(str(int(speed)), True, (0, 0, 0))
    screen.blit(speed_text, (center_x - speed_text.get_width() // 2 + S(3), center_y + main_bg_y_offset + S(38)))
    kmh_text = font_small.render("KMH", True, TEXT_COLOR)
    screen.blit(kmh_text, (center_x - kmh_text.get_width() // 2, center_y + main_bg_y_offset + S(125)))

    draw_cruise_set((WIDTH // 2 + S(190), HEIGHT // 2 + S(82)), font_large)

    # --- Clutch Indicator ---
    clutch_label = font_small.render("Clutch", True, TEXT_COLOR)
    clutch_text = font_small.render("Pressed" if clutch_pressed else "Released", True, RED if clutch_pressed else GREEN)
    screen.blit(clutch_label, (S(60), HEIGHT - S(160)))
    screen.blit(clutch_text, (S(60), HEIGHT - S(135)))

    # --- Brake Indicator ---
    brake_label = font_small.render("Brake", True, TEXT_COLOR)
    brake_text = font_small.render("Pressed" if brake_pressed else "Released", True, RED if brake_pressed else GREEN)
    screen.blit(brake_label, (WIDTH - S(160), HEIGHT - S(160)))
    screen.blit(brake_text, (WIDTH - S(160), HEIGHT - S(135)))

    # --- Bottom Buttons ---
    button_width = S(200)
    button_height = S(50)
    button_y = S(500)  # same as the other layouts (read.py click area)

    # CarPlay Button
    pygame.draw.rect(screen, BUTTON_COLOR, (S(50), button_y, button_width, button_height), border_radius=S(10))
    carplay_text = font_small.render("Apple CarPlay", True, BUTTON_TEXT_COLOR)
    carplay_rect = carplay_text.get_rect(center=(S(50) + button_width // 2, button_y + button_height // 2))
    screen.blit(carplay_text, carplay_rect)

    # Settings Button
    pygame.draw.rect(screen, BUTTON_COLOR, (WIDTH - S(50) - button_width, button_y, button_width, button_height), border_radius=S(10))
    settings_text = font_small.render("Settings", True, BUTTON_TEXT_COLOR)
    settings_rect = settings_text.get_rect(center=(WIDTH - S(50) - button_width // 2, button_y + button_height // 2))
    screen.blit(settings_text, settings_rect)

    # Tools Button (Top-right)
    tools_rect = pygame.Rect(WIDTH - S(150), S(50), S(100), S(30))
    pygame.draw.rect(screen, BUTTON_COLOR, tools_rect, border_radius=S(5))
    tools_text = font_small.render("Tools", True, BUTTON_TEXT_COLOR)
    text_rect = tools_text.get_rect(center=tools_rect.center)
    screen.blit(tools_text, text_rect)

    # --- Version ---
    version_text = font_small.render(f"Version: {settings_json['Program']['version']}", True, TEXT_COLOR)
    screen.blit(version_text, (WIDTH // 2 - version_text.get_width() // 2, HEIGHT - S(50)))

# --- Modern layout helpers ---
MODERN_ACCENT = (0, 200, 255)
MODERN_GREEN = (0, 220, 120)
MODERN_TRACK = (38, 44, 58)
MODERN_DIM_TEXT = (130, 140, 160)
MODERN_RED = (255, 60, 70)

font_speed = pygame.font.Font(None, S(190))
font_tiny = pygame.font.Font(None, S(24))

_modern_background = None

def _modern_bg():
    # vertical gradient, rendered once
    global _modern_background
    if _modern_background is None:
        _modern_background = pygame.Surface((WIDTH, HEIGHT))
        top, bottom = (16, 21, 34), (5, 7, 12)
        for y in range(HEIGHT):
            t = y / HEIGHT
            color = tuple(int(top[i] + (bottom[i] - top[i]) * t) for i in range(3))
            pygame.draw.line(_modern_background, color, (0, y), (WIDTH, y))
    return _modern_background

def _polar(center, radius, deg):
    rad = math.radians(deg)
    return (center[0] + radius * math.cos(rad), center[1] + radius * math.sin(rad))

def _ring_segment(center, r_outer, width, deg_start, deg_end, color, round_caps=True):
    # thick arc drawn as a polygon strip, angles clockwise on screen
    if deg_end <= deg_start:
        return
    steps = max(2, int((deg_end - deg_start) / 3) + 1)
    outer, inner = [], []
    for i in range(steps + 1):
        deg = deg_start + (deg_end - deg_start) * i / steps
        outer.append(_polar(center, r_outer, deg))
        inner.append(_polar(center, r_outer - width, deg))
    pygame.draw.polygon(screen, color, outer + inner[::-1])
    if round_caps:
        r_mid = r_outer - width / 2
        for deg in (deg_start, deg_end):
            pygame.draw.circle(screen, color, _polar(center, r_mid, deg), width // 2)

# Gauges sweep 270 degrees with the gap at the bottom
_GAUGE_START = 135
_GAUGE_SWEEP = 270

def _modern_gauge(center, radius, fraction, color, ticks, red_from=None):
    width = S(16)
    fraction = max(0.0, min(1.0, fraction))

    _ring_segment(center, radius, width, _GAUGE_START, _GAUGE_START + _GAUGE_SWEEP, MODERN_TRACK)
    if red_from is not None:
        _ring_segment(center, radius, width, _GAUGE_START + red_from * _GAUGE_SWEEP,
                      _GAUGE_START + _GAUGE_SWEEP, (90, 30, 40))
    if fraction > 0:
        _ring_segment(center, radius, width, _GAUGE_START, _GAUGE_START + fraction * _GAUGE_SWEEP, color)

    for i in range(ticks + 1):
        deg = _GAUGE_START + _GAUGE_SWEEP * i / ticks
        pygame.draw.line(screen, MODERN_DIM_TEXT, _polar(center, radius + S(8), deg), _polar(center, radius + S(16), deg), S(2))

def modern_dashboard(throttle, speed, rpm, clutch_pressed, brake_pressed, gear):
    screen.blit(_modern_bg(), (0, 0))

    # --- Title ---
    title_text = font_small.render("FORD FIESTA MK6 SPORT", True, MODERN_DIM_TEXT)
    screen.blit(title_text, (S(50), S(55)))
    pygame.draw.line(screen, MODERN_ACCENT, (S(50), S(84)), (S(110), S(84)), S(3))

    # --- Tools Button ---
    tools_button_rect = pygame.Rect(WIDTH - S(150), S(50), S(100), S(30))
    pygame.draw.rect(screen, BUTTON_COLOR, tools_button_rect, border_radius=S(10))
    tools_text = font_small.render("Tools", True, BUTTON_TEXT_COLOR)
    screen.blit(tools_text, tools_text.get_rect(center=tools_button_rect.center))

    # ============================================================
    #                    RPM GAUGE (LEFT)
    # ============================================================
    rpm_max = 6500
    rpm_center = (S(215), S(280))
    rpm_color = MODERN_RED if rpm > 5000 else MODERN_ACCENT
    _modern_gauge(rpm_center, S(130), rpm / rpm_max, rpm_color, 13, red_from=5000 / rpm_max)

    for i in range(0, 7):
        label = font_tiny.render(str(i), True, MODERN_DIM_TEXT)
        pos = _polar(rpm_center, S(98), _GAUGE_START + _GAUGE_SWEEP * i * 1000 / rpm_max)
        screen.blit(label, label.get_rect(center=pos))

    rpm_text = font_large.render(str(int(rpm)), True, TEXT_COLOR)
    screen.blit(rpm_text, rpm_text.get_rect(center=(rpm_center[0], rpm_center[1] + S(5))))
    rpm_label = font_tiny.render("RPM", True, MODERN_DIM_TEXT)
    screen.blit(rpm_label, rpm_label.get_rect(center=(rpm_center[0], rpm_center[1] + S(100))))

    # ============================================================
    #                    THROTTLE GAUGE (RIGHT)
    # ============================================================
    throttle_center = (WIDTH - S(215), S(280))
    _modern_gauge(throttle_center, S(130), throttle / 100, MODERN_GREEN, 4)

    throttle_text = font_large.render(f"{int(throttle)}%", True, TEXT_COLOR)
    screen.blit(throttle_text, throttle_text.get_rect(center=(throttle_center[0], throttle_center[1] + S(5))))
    throttle_label = font_tiny.render("THROTTLE", True, MODERN_DIM_TEXT)
    screen.blit(throttle_label, throttle_label.get_rect(center=(throttle_center[0], throttle_center[1] + S(100))))

    # ============================================================
    #                    SPEED + GEAR (CENTER)
    # ============================================================
    speed_color = MODERN_RED if speed > 120 else TEXT_COLOR
    speed_text = font_speed.render(str(int(speed)), True, speed_color)
    screen.blit(speed_text, speed_text.get_rect(center=(WIDTH // 2, S(215))).topleft)

    kmh_text = font_small.render("km/h", True, MODERN_DIM_TEXT)
    screen.blit(kmh_text, kmh_text.get_rect(center=(WIDTH // 2, S(300))))

    gear_center = (WIDTH // 2, S(370))
    gear_color = MODERN_GREEN if rpm >= 1250 else TEXT_COLOR
    pygame.draw.circle(screen, MODERN_TRACK, gear_center, S(38))
    pygame.draw.circle(screen, gear_color, gear_center, S(38), S(3))
    gear_str = str(gear) if gear != -1 else "N"
    gear_text = font_super_large.render(gear_str, True, gear_color)
    screen.blit(gear_text, gear_text.get_rect(center=gear_center))

    draw_cruise_set((WIDTH // 2, S(118)), font_large)

    # ============================================================
    #                    CLUTCH & BRAKE PILLS
    # ============================================================
    for label, pressed, x in (("CLUTCH", clutch_pressed, WIDTH // 2 - S(80)), ("BRAKE", brake_pressed, WIDTH // 2 + S(80))):
        pill = pygame.Rect(0, 0, S(130), S(32))
        pill.center = (x, S(450))
        pygame.draw.rect(screen, MODERN_RED if pressed else MODERN_TRACK, pill, border_radius=S(16))
        text = font_tiny.render(label, True, TEXT_COLOR if pressed else MODERN_DIM_TEXT)
        screen.blit(text, text.get_rect(center=pill.center))

    # ============================================================
    #                       BOTTOM BUTTONS
    # ============================================================
    button_width = S(200)
    button_height = S(50)

    # CarPlay
    pygame.draw.rect(screen, BUTTON_COLOR, (S(50), S(500), button_width, button_height), border_radius=S(10))
    carplay_text = font_small.render("Apple CarPlay", True, BUTTON_TEXT_COLOR)
    screen.blit(carplay_text, carplay_text.get_rect(center=(S(50) + button_width//2, S(500)+button_height//2)))

    # Settings
    pygame.draw.rect(screen, BUTTON_COLOR, (WIDTH - S(50) - button_width, S(500), button_width, button_height), border_radius=S(10))
    settings_text = font_small.render("Settings", True, BUTTON_TEXT_COLOR)
    screen.blit(settings_text, settings_text.get_rect(center=(WIDTH - S(50) - button_width//2, S(500)+button_height//2)))

    # Version
    version_text = font_tiny.render(f"Version: {settings_json['Program']['version']}", True, MODERN_DIM_TEXT)
    screen.blit(version_text, version_text.get_rect(center=(WIDTH // 2, S(526))))

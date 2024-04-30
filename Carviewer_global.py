import pygame
import subprocess
import json

# Initialize Pygame
pygame.init()

# Fonts
font_large = pygame.font.Font(None, 48)
font_small = pygame.font.Font(None, 36)

# Colors
BACKGROUND_COLOR = (30, 30, 30)
TEXT_COLOR = (255, 255, 255)
BUTTON_COLOR = (50, 50, 50)
BUTTON_TEXT_COLOR = (255, 255, 255)

# Screen dimensions
WIDTH, HEIGHT = 1024, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Carviewer 98-RS-RV")

def load_json():
    # read json
    with open("settings.json", "r") as file:
        return json.load(file)

def sendmessage(message):
    subprocess.Popen(['notify-send', message])
    return

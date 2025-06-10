from luma.led_matrix.device import max7219
from luma.core.interface.serial import bitbang
from luma.core.render import canvas
from PIL import Image

def load_json():
    # read json
    with open("settings.json", "r") as file:
        return json.load(file)

settings_json = load_json()

max7219_din = settings_json["GPIO"]["max7219_din"]
max7219_cs = settings_json["GPIO"]["max7219_cs"]
max7219_clk = settings_json["GPIO"]["max7219_clk"]

# CLK 11, CS 15, DIN 13
serial = bitbang(SCLK=max7219_clk, SDA=max7219_din, CE=max7219_cs)
device = max7219(serial, cascaded=1, rotate=0)
device.contrast(255)

gears = {
    "1": [
        "00011000",
        "00111000",
        "01111000",
        "00011000",
        "00011000",
        "00011000",
        "01111110",
        "01111110",
    ],
    "2": [
        "01111110",
        "11111111",
        "00000111",
        "00001110",
        "00011100",
        "00111000",
        "11111111",
        "11111111",
    ],
    "3": [
        "01111110",
        "11111111",
        "00000111",
        "00111110",
        "00000111",
        "00000111",
        "11111111",
        "01111110",
    ],
    "4": [
        "00011100",
        "00111100",
        "01111100",
        "11101111",
        "11111111",
        "00011100",
        "00011100",
        "00011100",
    ],
    "5": [
        "11111111",
        "11100000",
        "11111100",
        "11111110",
        "00000111",
        "00000111",
        "11111110",
        "01111100",
    ],
    # N
    "-1": [
        "11000011",
        "11100011",
        "11110011",
        "11011011",
        "11001111",
        "11000111",
        "11000011",
        "11000011",
    ]
}

def draw_gear(gear_id):
    pixels = gears[str(gear_id)]
    
    # Create a new 8x8 1-bit image
    image = Image.new("1", (8, 8))
    for y, row in enumerate(pixels):
        for x, bit in enumerate(row):
            image.putpixel((x, y), int(bit))

    # Draw bitmap onto device
    with canvas(device) as draw:
        draw.bitmap((0, 0), image, fill="white")

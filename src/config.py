import sys
from json import loads, load
from pkgutil import get_data
from io import BytesIO

import pygame

COMPILED = getattr(sys, "frozen", False)

if COMPILED:
    embedded_path = sys._MEIPASS
    data_path = f"{embedded_path}/data"
    ASSETS_PATH = f"{embedded_path}/assets"
else:
    data_path = "./data"    
    ASSETS_PATH = "./assets"
    
with open(f"{data_path}/config.json") as config:
        config_data = load(config)

with open(f"{data_path}/levels.json") as levels:
        levels_data = load(levels)

WIDTH = config_data["size"]["width"]
HEIGHT = config_data["size"]["height"]
SIZE = (WIDTH, HEIGHT)
MIN_RATIO = (min(WIDTH, HEIGHT))/512
MAX_RATIO = (max(WIDTH, HEIGHT))/512
X_RATIO = WIDTH/512
Y_RATIO = HEIGHT/512

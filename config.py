from json import load

with open("config.json") as config:
    config_data = load(config)

WIDTH = config_data["config"]["size"]["width"]
HEIGHT = config_data["config"]["size"]["height"]
SIZE = (WIDTH, HEIGHT)
MIN_RATIO = (min(WIDTH, HEIGHT))/512
MAX_RATIO = (max(WIDTH, HEIGHT))/512
X_RATIO = WIDTH/512
Y_RATIO = HEIGHT/512

levels_data = config_data["levels"]

# levels = [
#     Level(lv["name"], lv["args"]) for lv in levels_data
# ]
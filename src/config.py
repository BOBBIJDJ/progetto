import sys
from json import loads, load, dumps

from cryptography.fernet import Fernet

COMPILED = getattr(sys, "frozen", False)

if COMPILED:
    embedded_path = sys._MEIPASS
    data_path = f"{embedded_path}/data"
    key_path = f"{embedded_path}/key"
    ASSETS_PATH = f"{embedded_path}/assets"
else:
    data_path = "./data"   
    key_path = "./key" 
    ASSETS_PATH = "./assets"

with open(f"{key_path}/key.key", "rb") as key_file:
    KEY = key_file.read()
    fernet = Fernet(KEY)
    
with open(f"{data_path}/config.json") as config:
    config_data = load(config)

with open(f"{data_path}/levels.json") as levels:
    default_levels_data = load(levels)

try:
    with open(f"./save.save", "rb") as save:
        encrypted_save = save.read()
        decrypted_save = fernet.decrypt(encrypted_save)
        loaded_levels_data = loads(decrypted_save.decode("utf-8"))
    LOADED = True
except FileNotFoundError:
    loaded_levels_data = None
    LOADED = False

WIDTH = config_data["size"]["width"]
HEIGHT = config_data["size"]["height"]
SIZE = (WIDTH, HEIGHT)
MAX_RATIO = (max(WIDTH, HEIGHT))/512
X_RATIO = WIDTH/512
Y_RATIO = HEIGHT/512

def saveState(
    save_data : dict,
) -> None:
    json_save = dumps(save_data).encode("utf-8")
    encrypted_save = fernet.encrypt(json_save)
    with open("./save.save", "wb") as save:
        save.write(encrypted_save)

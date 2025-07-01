config = open("config.txt")
SIZE = (WIDTH, HEIGHT) = tuple(
    int(size) for size in config.read().split(","))
MIN_RATIO = (min(WIDTH, HEIGHT))/512
MAX_RATIO = (max(WIDTH, HEIGHT))/512
X_RATIO = WIDTH/512
Y_RATIO = HEIGHT/512
config.close()
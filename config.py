# class Config:
#     def __init__(self):
#         with open("config.txt") as config:
#             self.SIZE = (self.WIDTH, self.HEIGHT) = tuple(
#                 int(size) for size in config.read().split(",")
#             )
#         self.MIN_RATIO = (min(self.WIDTH, self.HEIGHT))/512
#         self.MAX_RATIO = (max(self.WIDTH, self.HEIGHT))/512
#         self.X_RATIO = self.WIDTH/512
#         self.Y_RATIO = self.HEIGHT/512

# config = Config()

# def init() -> Config:
#     return config

config = open("config.txt")
SIZE = (WIDTH, HEIGHT) = tuple(
    int(size) for size in config.read().split(",")
)
MIN_RATIO = (min(WIDTH, HEIGHT))/512
MAX_RATIO = (max(WIDTH, HEIGHT))/512
X_RATIO = WIDTH/512
Y_RATIO = HEIGHT/512
config.close()
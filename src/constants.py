# Dimensions
from src.util.vec2d import Vec2d


TILE_SIZE = 64
GRID_SIZE_X = 14
GRID_SIZE_Y = 10

CENTER_X = (GRID_SIZE_X // 2) * TILE_SIZE
CENTER_Y = (GRID_SIZE_Y // 2) * TILE_SIZE

MIN_X = 0
MAX_X = 700
MIN_Y = 50
MAX_Y = 350

FLOOR_MIN_X = 50
FLOOR_MIN_Y = 130


# Colors
BLACK = (18,8,6,255)
WHITE = (245, 217, 171, 1)
YELLOW = (234,175,55,255)
BURGUNDY = (144,8,5,255)
RED_BLACK = (111, 5, 1)

# Seats
SEAT_1 = Vec2d(50, 520)
SEAT_2 = Vec2d(200, 520)
SEAT_3 = Vec2d(350, 520)
SEAT_4 = Vec2d(500, 520)
SEAT_5 = Vec2d(640, 520)


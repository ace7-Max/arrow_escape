# config.py
# 全局配置常量
WINDOW_WIDTH = 520
WINDOW_HEIGHT = 700
FPS = 60
TITLE = "箭头消除 · 方向突围"

ROWS = 5
COLS = 5
CELL_SIZE = 68
CELL_GAP = 6
BOARD_PADDING = 16
BOARD_WIDTH = COLS * CELL_SIZE + (COLS - 1) * CELL_GAP + 2 * BOARD_PADDING
BOARD_HEIGHT = ROWS * CELL_SIZE + (ROWS - 1) * CELL_GAP + 2 * BOARD_PADDING
BOARD_X = (WINDOW_WIDTH - BOARD_WIDTH) // 2
BOARD_Y = 110

MAX_MISTAKES = 3
TOTAL_LEVELS = 6

DIRS = {
    'up':    {'dr': -1, 'dc': 0,  'symbol': '↑'},
    'down':  {'dr': 1,  'dc': 0,  'symbol': '↓'},
    'left':  {'dr': 0,  'dc': -1, 'symbol': '←'},
    'right': {'dr': 0,  'dc': 1,  'symbol': '→'},
}
DIR_NAMES = list(DIRS.keys())

COLOR_BG         = (15, 26, 36)
COLOR_BOARD_BG   = (24, 49, 61)
COLOR_CELL       = (37, 78, 96)
COLOR_CELL_HOVER = (52, 100, 120)
COLOR_BLOCKED    = (179, 65, 65)
COLOR_TEXT       = (217, 234, 245)
COLOR_TEXT_DIM   = (150, 180, 200)
COLOR_ARROW = {
    'up':    (255, 217, 102),
    'down':  (176, 229, 124),
    'left':  (255, 176, 124),
    'right': (124, 198, 255),
}
COLOR_WIN  = (179, 255, 155)
COLOR_FAIL = (255, 167, 167)

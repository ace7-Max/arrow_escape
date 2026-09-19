# model/rules.py
# 四个方向的路径检测
from config import ROWS, COLS, DIRS


def inside(r, c):
    return 0 <= r < ROWS and 0 <= c < COLS


def is_blocked(board, r, c, direction):
    dr = DIRS[direction]['dr']
    dc = DIRS[direction]['dc']
    nr, nc = r + dr, c + dc
    while inside(nr, nc):
        if not board.is_empty(nr, nc):
            return True
        nr += dr
        nc += dc
    return False


def is_all_cleared(board):
    return board.count_arrows() == 0


def calc_arrow_count(level):
    """
    每一关的箭头数量。
    下限 7，之后每关 +2，上限 18（5×5 棋盘放太多会无解）。
    """
    return min(7 + (level - 1) * 2, 18)


def has_blocked_arrow(board):
    """当前棋盘上是否存在至少一个被阻挡的箭头"""
    for r in range(ROWS):
        for c in range(COLS):
            cell = board.get(r, c)
            if cell is None:
                continue
            if is_blocked(board, r, c, cell['dir']):
                return True
    return False


def count_blocked_arrows(board):
    """统计当前被阻挡的箭头数量"""
    n = 0
    for r in range(ROWS):
        for c in range(COLS):
            cell = board.get(r, c)
            if cell is None:
                continue
            if is_blocked(board, r, c, cell['dir']):
                n += 1
    return n


def is_solvable(board):
    """
    贪心求解器：反复找“当前能飞出的箭头”，飞掉，再看新的。
    如果最后全部飞光，就可解；否则无解。不修改传入的 board。
    """
    grid = [[board.grid[r][c] for c in range(COLS)] for r in range(ROWS)]

    def blocked_sim(r, c, direction):
        dr = DIRS[direction]['dr']
        dc = DIRS[direction]['dc']
        nr, nc = r + dr, c + dc
        while 0 <= nr < ROWS and 0 <= nc < COLS:
            if grid[nr][nc] is not None:
                return True
            nr += dr
            nc += dc
        return False

    while True:
        removable = []
        for r in range(ROWS):
            for c in range(COLS):
                cell = grid[r][c]
                if cell is None:
                    continue
                if not blocked_sim(r, c, cell['dir']):
                    removable.append((r, c))

        if not removable:
            for r in range(ROWS):
                for c in range(COLS):
                    if grid[r][c] is not None:
                        return False
            return True

        for r, c in removable:
            grid[r][c] = None

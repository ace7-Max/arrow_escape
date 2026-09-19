# model/board.py
import random
from config import ROWS, COLS, DIR_NAMES


class Board:
    def __init__(self):
        self.grid = [[None] * COLS for _ in range(ROWS)]

    def clear(self):
        for r in range(ROWS):
            for c in range(COLS):
                self.grid[r][c] = None

    def get(self, r, c):
        if 0 <= r < ROWS and 0 <= c < COLS:
            return self.grid[r][c]
        return None

    def set(self, r, c, value):
        self.grid[r][c] = value

    def remove(self, r, c):
        self.grid[r][c] = None

    def is_empty(self, r, c):
        return self.grid[r][c] is None

    def count_arrows(self):
        n = 0
        for r in range(ROWS):
            for c in range(COLS):
                if self.grid[r][c] is not None:
                    n += 1
        return n

    def _fill_random(self, n):
        self.clear()
        candidates = [(r, c) for r in range(ROWS) for c in range(COLS)]
        random.shuffle(candidates)
        for i in range(n):
            r, c = candidates[i]
            self.grid[r][c] = {'dir': random.choice(DIR_NAMES)}

    def place_random(self, n, level=1, max_tries=3000):
        """
        生成一个满足以下条件的棋盘：
          1. 有解（存在消除顺序）
          2. 至少有 min_blocked 个箭头当前被阻挡
        min_blocked 按关卡提升：第 1 关 2 个，之后每关 +1，最多 n-1 个。
        """
        from model.rules import is_solvable, count_blocked_arrows

        # 关卡越高，要求被阻挡的箭头越多
        min_blocked = min(2 + (level - 1), n - 1)
        # 同时不允许超过全部箭头（至少留 1 个能飞）
        min_blocked = min(min_blocked, n - 1)

        fallback = None
        fallback_score = -1

        for _ in range(max_tries):
            self._fill_random(n)
            if not is_solvable(self):
                continue
            blocked = count_blocked_arrows(self)
            if blocked >= min_blocked:
                return
            # 记录“最接近要求”的一局，做兜底
            if blocked > fallback_score:
                fallback_score = blocked
                fallback = [row[:] for row in self.grid]

        # 兜底：用遇到过的最好结果
        if fallback is not None:
            self.grid = fallback
# view/effects.py
# 飞出与碰撞动画
from config import (
    CELL_SIZE, CELL_GAP, BOARD_PADDING,
    WINDOW_WIDTH, BOARD_WIDTH, BOARD_HEIGHT,
    ROWS, COLS, DIRS
)


class FlyingArrow:
    def __init__(self, cx, cy, direction, dx, dy, total_frames):
        self.cx = float(cx)
        self.cy = float(cy)
        self.direction = direction
        self.dx = dx
        self.dy = dy
        self.progress = 0
        self.total_frames = max(1, total_frames)
        self.alive = True

    def update(self):
        self.progress += 1
        t = self.progress / self.total_frames
        speed = 0.9 + t * 0.6
        self.cx += self.dx * speed
        self.cy += self.dy * speed
        if self.progress >= self.total_frames:
            self.alive = False


class BounceArrow:
    """
    被阻挡的箭头：
    从起点飞到阻挡物边缘（forward_px 由外部计算好），再原路返回。
    """
    def __init__(self, cx, cy, direction, dx, dy, forward_px, total_frames=40):
        self.cx = float(cx)
        self.cy = float(cy)
        self.origin_cx = float(cx)
        self.origin_cy = float(cy)
        self.direction = direction
        self.dx = dx
        self.dy = dy
        self.progress = 0
        self.total_frames = total_frames
        self.forward_px = forward_px
        self.alive = True

    def update(self):
        self.progress += 1
        t = self.progress / self.total_frames
        # 前 45% 前进（缓出），后 55% 返回（缓入）
        if t <= 0.45:
            k = t / 0.45
            k = 1 - (1 - k) * (1 - k)   # ease-out
            offset = self.forward_px * k
        else:
            k = (t - 0.45) / 0.55
            k = k * k                    # ease-in
            offset = self.forward_px * (1 - k)
        self.cx = self.origin_cx + self.dx * offset
        self.cy = self.origin_cy + self.dy * offset
        if self.progress >= self.total_frames:
            self.alive = False


class EffectManager:
    def __init__(self):
        self.blocked = {}
        self.flying = []
        self.bouncing = []

    def trigger_blocked(self, r, c, direction, board):
        """计算「飞到阻挡物边缘」的距离，创建反弹动画"""
        self.blocked[(r, c)] = 22

        target_r, target_c = self._find_blocker(board, r, c, direction)
        if target_r is None:
            return

        cx, cy = self._cell_center(r, c)
        bx, by = self._cell_center(target_r, target_c)
        full_dist = ((bx - cx) ** 2 + (by - cy) ** 2) ** 0.5

        buffer = CELL_SIZE - 14
        forward_px = max(6, full_dist - buffer)

        dx, dy = self._unit_offset(direction)
        self.bouncing.append(
            BounceArrow(cx, cy, direction, dx, dy, forward_px, total_frames=40)
        )

    def trigger_fly_out(self, r, c, direction):
        cx, cy = self._cell_center(r, c)
        dx, dy = self._unit_offset(direction)
        px = self._pixels_to_exit(r, c, direction)
        # 上一版 4.5，再快 1.5 倍 → 6.75
        speed = 6.75
        total_frames = max(18, int(px / speed))
        self.flying.append(
            FlyingArrow(cx, cy, direction, dx * speed, dy * speed, total_frames)
        )

    def update(self):
        for key in list(self.blocked.keys()):
            self.blocked[key] -= 1
            if self.blocked[key] <= 0:
                del self.blocked[key]
        for f in self.flying[:]:
            f.update()
            if not f.alive:
                self.flying.remove(f)
        for b in self.bouncing[:]:
            b.update()
            if not b.alive:
                self.bouncing.remove(b)

    def blocked_cells(self):
        return set(self.blocked.keys())

    def get_flying(self):
        return self.flying

    def get_bouncing(self):
        return self.bouncing

    def _find_blocker(self, board, r, c, direction):
        dr, dc = DIRS[direction]['dr'], DIRS[direction]['dc']
        nr, nc = r + dr, c + dc
        while 0 <= nr < ROWS and 0 <= nc < COLS:
            if not board.is_empty(nr, nc):
                return nr, nc
            nr += dr
            nc += dc
        return None, None

    def _cell_center(self, r, c):
        board_x = (WINDOW_WIDTH - BOARD_WIDTH) // 2
        board_y = 130
        x = board_x + BOARD_PADDING + c * (CELL_SIZE + CELL_GAP) + CELL_SIZE // 2
        y = board_y + BOARD_PADDING + r * (CELL_SIZE + CELL_GAP) + CELL_SIZE // 2
        return x, y

    def _unit_offset(self, direction):
        if direction == 'up':    return 0, -1
        if direction == 'down':  return 0,  1
        if direction == 'left':  return -1, 0
        if direction == 'right': return 1,  0
        return 0, 0

    def _pixels_to_exit(self, r, c, direction):
        board_x = (WINDOW_WIDTH - BOARD_WIDTH) // 2
        board_y = 130
        x = board_x + BOARD_PADDING + c * (CELL_SIZE + CELL_GAP) + CELL_SIZE // 2
        y = board_y + BOARD_PADDING + r * (CELL_SIZE + CELL_GAP) + CELL_SIZE // 2
        margin = 80
        left   = board_x - margin
        right  = board_x + BOARD_WIDTH + margin
        top    = board_y - margin
        bottom = board_y + BOARD_HEIGHT + margin
        if direction == 'up':    return y - top
        if direction == 'down':  return bottom - y
        if direction == 'left':  return x - left
        if direction == 'right': return right - x
        return 300

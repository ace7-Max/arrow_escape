# view/renderer.py
import os
import pygame
from config import (
    WINDOW_WIDTH, WINDOW_HEIGHT,
    BOARD_WIDTH, BOARD_HEIGHT, BOARD_PADDING,
    ROWS, COLS, CELL_SIZE, CELL_GAP, DIRS,
    COLOR_BG, COLOR_BOARD_BG, COLOR_CELL, COLOR_CELL_HOVER,
    COLOR_TEXT, COLOR_TEXT_DIM, COLOR_ARROW, COLOR_BLOCKED,
    COLOR_WIN, COLOR_FAIL, MAX_MISTAKES
)

BOARD_X = (WINDOW_WIDTH - BOARD_WIDTH) // 2
BOARD_Y = 130

COLOR_BTN       = (45, 92, 114)
COLOR_BTN_HOVER = (60, 120, 150)
COLOR_BTN_TEXT  = (240, 250, 255)

MAX_LEVEL_BUTTONS = 6


def _load_font(size):
    candidates = [
        r"C:\Windows\Fonts\msyh.ttc",
        r"C:\Windows\Fonts\msyhbd.ttc",
        r"C:\Windows\Fonts\simhei.ttf",
        r"C:\Windows\Fonts\simsun.ttc",
    ]
    for path in candidates:
        if os.path.exists(path):
            try:
                return pygame.font.Font(path, size)
            except Exception:
                continue
    return pygame.font.Font(None, size)


class Renderer:
    def __init__(self, screen, game):
        self.screen = screen
        self.game = game
        self.font_arrow = _load_font(52)
        self.font_ui    = _load_font(20)
        self.font_mid   = _load_font(24)
        self.font_big   = _load_font(34)
        self.font_huge  = _load_font(50)
        self._effects = None

    def set_effects(self, effects):
        self._effects = effects

    # ── 坐标 ──
    def cell_rect(self, r, c):
        x = BOARD_X + BOARD_PADDING + c * (CELL_SIZE + CELL_GAP)
        y = BOARD_Y + BOARD_PADDING + r * (CELL_SIZE + CELL_GAP)
        return pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)

    def _cell_center(self, r, c):
        x = BOARD_X + BOARD_PADDING + c * (CELL_SIZE + CELL_GAP) + CELL_SIZE // 2
        y = BOARD_Y + BOARD_PADDING + r * (CELL_SIZE + CELL_GAP) + CELL_SIZE // 2
        return x, y

    def hit_test(self, pos):
        for r in range(ROWS):
            for c in range(COLS):
                if self.cell_rect(r, c).collidepoint(pos):
                    return r, c
        return None

    # ── 通用 ──
    def draw_text(self, text, font, color, center=None, topleft=None):
        surf = font.render(text, True, color)
        if center:
            rect = surf.get_rect(center=center)
        else:
            rect = surf.get_rect(topleft=topleft)
        self.screen.blit(surf, rect)
        return rect

    def draw_button(self, rect, text, font, hover=False):
        color = COLOR_BTN_HOVER if hover else COLOR_BTN
        pygame.draw.rect(self.screen, color, rect, border_radius=20)
        pygame.draw.rect(self.screen, (10, 30, 40), rect, 2, border_radius=20)
        surf = font.render(text, True, COLOR_BTN_TEXT)
        self.screen.blit(surf, surf.get_rect(center=rect.center))

    def _draw_arrow_at(self, direction, center):
        symbol = DIRS[direction]['symbol']
        color = COLOR_ARROW[direction]
        text = self.font_arrow.render(symbol, True, color)
        self.screen.blit(text, text.get_rect(center=(int(center[0]), int(center[1]))))

    # ── 开始界面 ──
    def draw_start_screen(self, mouse_pos, start_rect, select_rect, quit_rect):
        self.screen.fill(COLOR_BG)
        self.draw_text('箭头突围', self.font_huge, COLOR_TEXT,
                       center=(WINDOW_WIDTH // 2, 160))
        self.draw_text('点击箭头，让它飞出棋盘', self.font_mid, COLOR_TEXT_DIM,
                       center=(WINDOW_WIDTH // 2, 240))
        self.draw_text('前方有箭头阻挡时无法飞出', self.font_mid, COLOR_TEXT_DIM,
                       center=(WINDOW_WIDTH // 2, 280))
        self.draw_text('失误 ' + str(MAX_MISTAKES) + ' 次本关失败',
                       self.font_mid, COLOR_FAIL,
                       center=(WINDOW_WIDTH // 2, 320))

        hover1 = start_rect.collidepoint(mouse_pos)
        self.draw_button(start_rect, '开始游戏', self.font_big, hover1)
        hover2 = select_rect.collidepoint(mouse_pos)
        self.draw_button(select_rect, '选择关卡', self.font_big, hover2)
        hover3 = quit_rect.collidepoint(mouse_pos)
        self.draw_button(quit_rect, '退出游戏', self.font_big, hover3)

    # ── 关卡选择界面 ──
    def draw_level_select_screen(self, mouse_pos, level_rects, back_rect):
        self.screen.fill(COLOR_BG)
        self.draw_text('选择关卡', self.font_huge, COLOR_TEXT,
                       center=(WINDOW_WIDTH // 2, 130))
        self.draw_text('点击进入对应关卡', self.font_mid, COLOR_TEXT_DIM,
                       center=(WINDOW_WIDTH // 2, 190))

        for idx, rect in enumerate(level_rects):
            hover = rect.collidepoint(mouse_pos)
            self.draw_button(rect, '第 ' + str(idx + 1) + ' 关', self.font_mid, hover)

        hover_back = back_rect.collidepoint(mouse_pos)
        self.draw_button(back_rect, '返回', self.font_mid, hover_back)

    # ── 游戏界面（含 重新开始 + 返回首页 两个按钮）──
    def draw_game_screen(self, mouse_pos, restart_rect, home_rect,
                         blocked_cells=None, hover_cell=None):
        if blocked_cells is None:
            blocked_cells = set()
        self.screen.fill(COLOR_BG)
        g = self.game

        self.draw_text('第 ' + str(g.level) + ' 关',
                       self.font_big, COLOR_TEXT,
                       center=(WINDOW_WIDTH // 2, 40))

        self.draw_text('剩余箭头: ' + str(g.board.count_arrows()),
                       self.font_ui, COLOR_TEXT,
                       topleft=(BOARD_X, 88))
        self.draw_text('剩余失误: ' + str(MAX_MISTAKES - g.mistakes),
                       self.font_ui, COLOR_TEXT,
                       topleft=(BOARD_X + BOARD_WIDTH - 130, 88))

        board_rect = pygame.Rect(BOARD_X, BOARD_Y, BOARD_WIDTH, BOARD_HEIGHT)
        pygame.draw.rect(self.screen, COLOR_BOARD_BG, board_rect, border_radius=28)

        bouncing_centers = set()
        if self._effects is not None:
            for b in self._effects.get_bouncing():
                bouncing_centers.add((b.origin_cx, b.origin_cy))

        for r in range(ROWS):
            for c in range(COLS):
                rect = self.cell_rect(r, c)
                cell = g.board.get(r, c)

                if (r, c) in blocked_cells:
                    color = COLOR_BLOCKED
                elif hover_cell == (r, c) and cell:
                    color = COLOR_CELL_HOVER
                else:
                    color = COLOR_CELL

                pygame.draw.rect(self.screen, color, rect, border_radius=18)
                pygame.draw.rect(self.screen, (10, 25, 32), rect, 2, border_radius=18)

                if cell:
                    cx, cy = self._cell_center(r, c)
                    if (cx, cy) in bouncing_centers:
                        continue
                    self._draw_arrow_at(cell['dir'], rect.center)

        if self._effects is not None:
            for f in self._effects.get_flying():
                self._draw_arrow_at(f.direction, (f.cx, f.cy))
            for b in self._effects.get_bouncing():
                self._draw_arrow_at(b.direction, (b.cx, b.cy))

        if g.feedback:
            color_map = {
                'info': COLOR_TEXT,
                'success': (180, 240, 180),
                'fail': COLOR_FAIL,
                'win': COLOR_WIN,
            }
            color = color_map.get(g.feedback_type, COLOR_TEXT_DIM)
            self.draw_text(g.feedback, self.font_mid, color,
                           center=(WINDOW_WIDTH // 2,
                                   BOARD_Y + BOARD_HEIGHT + 30))

        # 底部两个按钮
        hover_r = restart_rect.collidepoint(mouse_pos)
        self.draw_button(restart_rect, '重新开始 (R)', self.font_ui, hover_r)
        hover_h = home_rect.collidepoint(mouse_pos)
        self.draw_button(home_rect, '返回首页', self.font_ui, hover_h)

    # ── 关卡通过界面 ──
    def draw_level_clear_screen(self, mouse_pos, next_rect, home_rect):
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))

        self.draw_text('关卡完成！', self.font_huge, COLOR_WIN,
                       center=(WINDOW_WIDTH // 2, 250))
        self.draw_text('第 ' + str(self.game.level) + ' 关通关',
                       self.font_mid, COLOR_TEXT,
                       center=(WINDOW_WIDTH // 2, 320))

        hover1 = next_rect.collidepoint(mouse_pos)
        self.draw_button(next_rect, '下一关', self.font_mid, hover1)
        hover2 = home_rect.collidepoint(mouse_pos)
        self.draw_button(home_rect, '返回首页', self.font_mid, hover2)

    # ── 全部通关界面 ──
    def draw_all_clear_screen(self, mouse_pos, home_rect):
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 190))
        self.screen.blit(overlay, (0, 0))

        self.draw_text('你已通过全部关卡！', self.font_huge, COLOR_WIN,
                       center=(WINDOW_WIDTH // 2, 300))
        self.draw_text('恭喜你，全部挑战成功！', self.font_mid, COLOR_TEXT_DIM,
                       center=(WINDOW_WIDTH // 2, 380))

        hover = home_rect.collidepoint(mouse_pos)
        self.draw_button(home_rect, '返回首页', self.font_mid, hover)

    # ── 失败界面 ──
    def draw_fail_screen(self, mouse_pos, retry_rect, home_rect):
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 170))
        self.screen.blit(overlay, (0, 0))

        self.draw_text('关卡失败', self.font_huge, COLOR_FAIL,
                       center=(WINDOW_WIDTH // 2, 250))
        self.draw_text('失误次数已用完', self.font_mid, COLOR_TEXT_DIM,
                       center=(WINDOW_WIDTH // 2, 320))
        self.draw_text('当前：第 ' + str(self.game.level) + ' 关',
                       self.font_mid, COLOR_TEXT,
                       center=(WINDOW_WIDTH // 2, 365))

        hover1 = retry_rect.collidepoint(mouse_pos)
        self.draw_button(retry_rect, '重玩本关', self.font_mid, hover1)
        hover2 = home_rect.collidepoint(mouse_pos)
        self.draw_button(home_rect, '返回首页', self.font_mid, hover2)

    # ── 工具 ──
    def make_level_buttons(self, total_levels):
        rects = []
        cols = 2
        btn_w, btn_h = 180, 56
        gap_x, gap_y = 40, 24
        start_y = 260
        for i in range(total_levels):
            row = i // cols
            col = i % cols
            x = WINDOW_WIDTH // 2 - (cols * btn_w + (cols - 1) * gap_x) // 2 \
                + col * (btn_w + gap_x)
            y = start_y + row * (btn_h + gap_y)
            rects.append(pygame.Rect(x, y, btn_w, btn_h))
        return rects
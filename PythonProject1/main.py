# main.py
import os
import sys

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import pygame

from config import WINDOW_WIDTH, WINDOW_HEIGHT, FPS, TITLE
from controller.game import Game, GameState
from view.renderer import Renderer
from view.effects import EffectManager


# 界面状态
SCREEN_START       = 'start'
SCREEN_SELECT      = 'select'
SCREEN_GAME        = 'game'
SCREEN_LEVEL_CLEAR = 'level_clear'
SCREEN_ALL_CLEAR   = 'all_clear'
SCREEN_FAIL        = 'fail'

TOTAL_LEVELS = 6


def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption(TITLE)
    clock = pygame.time.Clock()

    game = Game()
    renderer = Renderer(screen, game)
    effects = EffectManager()

    screen_mode = SCREEN_START
    pending_level_clear = False
    clear_timer = 0

    # ── 开始界面按钮 ──
    start_btn  = pygame.Rect(WINDOW_WIDTH // 2 - 110, 400, 220, 56)
    select_btn = pygame.Rect(WINDOW_WIDTH // 2 - 110, 480, 220, 56)
    quit_btn   = pygame.Rect(WINDOW_WIDTH // 2 - 110, 560, 220, 56)

    # ── 关卡选择界面 ──
    level_rects = renderer.make_level_buttons(TOTAL_LEVELS)
    select_back_btn = pygame.Rect(WINDOW_WIDTH // 2 - 90, 640, 180, 48)

    # ── 游戏界面底部两个按钮 ──
    btn_w, btn_h = 160, 44
    gap = 24
    total_w = btn_w * 2 + gap
    x0 = WINDOW_WIDTH // 2 - total_w // 2
    y0 = WINDOW_HEIGHT - 70
    restart_btn = pygame.Rect(x0, y0, btn_w, btn_h)
    game_home_btn = pygame.Rect(x0 + btn_w + gap, y0, btn_w, btn_h)

    # ── 弹窗按钮 ──
    next_btn      = pygame.Rect(WINDOW_WIDTH // 2 - 170, 440, 150, 52)
    home_btn      = pygame.Rect(WINDOW_WIDTH // 2 + 20,  440, 150, 52)
    all_home_btn  = pygame.Rect(WINDOW_WIDTH // 2 - 100, 440, 200, 56)
    retry_btn     = pygame.Rect(WINDOW_WIDTH // 2 - 170, 440, 150, 52)
    fail_home_btn = pygame.Rect(WINDOW_WIDTH // 2 + 20,  440, 150, 52)

    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()
        hover_cell = renderer.hit_test(mouse_pos) if screen_mode == SCREEN_GAME else None

        # ── 事件 ──
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if screen_mode == SCREEN_START:
                    if start_btn.collidepoint(event.pos):
                        game.start_level(1)
                        effects = EffectManager()
                        screen_mode = SCREEN_GAME
                        pending_level_clear = False
                    elif select_btn.collidepoint(event.pos):
                        screen_mode = SCREEN_SELECT
                    elif quit_btn.collidepoint(event.pos):
                        running = False

                elif screen_mode == SCREEN_SELECT:
                    if select_back_btn.collidepoint(event.pos):
                        screen_mode = SCREEN_START
                    else:
                        for idx, rect in enumerate(level_rects):
                            if rect.collidepoint(event.pos):
                                game.start_level(idx + 1)
                                effects = EffectManager()
                                screen_mode = SCREEN_GAME
                                pending_level_clear = False
                                break

                elif screen_mode == SCREEN_GAME:
                    # 返回首页按钮
                    if game_home_btn.collidepoint(event.pos):
                        screen_mode = SCREEN_START
                        effects = EffectManager()
                        pending_level_clear = False
                        continue
                    # 重新开始
                    if restart_btn.collidepoint(event.pos):
                        game.restart_level()
                        effects = EffectManager()
                        pending_level_clear = False
                        continue
                    # 点箭头
                    cell = renderer.hit_test(event.pos)
                    if cell is not None:
                        game.click_cell(cell[0], cell[1])

                elif screen_mode == SCREEN_LEVEL_CLEAR:
                    if next_btn.collidepoint(event.pos):
                        game.next_level()
                        effects = EffectManager()
                        pending_level_clear = False
                        if getattr(game, 'finished', False):
                            screen_mode = SCREEN_ALL_CLEAR
                        else:
                            screen_mode = SCREEN_GAME
                    elif home_btn.collidepoint(event.pos):
                        screen_mode = SCREEN_START
                        effects = EffectManager()
                        pending_level_clear = False

                elif screen_mode == SCREEN_ALL_CLEAR:
                    if all_home_btn.collidepoint(event.pos):
                        screen_mode = SCREEN_START
                        effects = EffectManager()

                elif screen_mode == SCREEN_FAIL:
                    if retry_btn.collidepoint(event.pos):
                        game.restart_level()
                        effects = EffectManager()
                        screen_mode = SCREEN_GAME
                    elif fail_home_btn.collidepoint(event.pos):
                        screen_mode = SCREEN_START
                        effects = EffectManager()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r and screen_mode == SCREEN_GAME:
                    game.restart_level()
                    effects = EffectManager()
                    pending_level_clear = False
                elif event.key == pygame.K_ESCAPE:
                    if screen_mode in (SCREEN_GAME, SCREEN_SELECT,
                                       SCREEN_LEVEL_CLEAR, SCREEN_FAIL,
                                       SCREEN_ALL_CLEAR):
                        screen_mode = SCREEN_START
                        effects = EffectManager()

        # ── 逻辑更新 ──
        if screen_mode == SCREEN_GAME:
            for anim in game.consume_animations():
                if anim[0] == 'blocked':
                    r, c, direction = anim[1], anim[2], anim[3]
                    effects.trigger_blocked(r, c, direction, game.board)
                elif anim[0] == 'fly_out':
                    r, c, direction = anim[1], anim[2], anim[3]
                    effects.trigger_fly_out(r, c, direction)
                elif anim[0] == 'win':
                    pending_level_clear = True
                    clear_timer = 50

            effects.update()

            if game.state == GameState.FAIL:
                screen_mode = SCREEN_FAIL
                pending_level_clear = False
            elif pending_level_clear:
                clear_timer -= 1
                if clear_timer <= 0:
                    pending_level_clear = False
                    screen_mode = SCREEN_LEVEL_CLEAR

        # ── 渲染 ──
        if screen_mode == SCREEN_START:
            renderer.draw_start_screen(mouse_pos, start_btn, select_btn, quit_btn)

        elif screen_mode == SCREEN_SELECT:
            renderer.draw_level_select_screen(mouse_pos, level_rects, select_back_btn)

        elif screen_mode == SCREEN_GAME:
            renderer.set_effects(effects)
            renderer.draw_game_screen(mouse_pos, restart_btn, game_home_btn,
                                      effects.blocked_cells(), hover_cell)

        elif screen_mode == SCREEN_LEVEL_CLEAR:
            renderer.set_effects(effects)
            renderer.draw_game_screen(mouse_pos, restart_btn, game_home_btn,
                                      effects.blocked_cells(), hover_cell)
            renderer.draw_level_clear_screen(mouse_pos, next_btn, home_btn)

        elif screen_mode == SCREEN_ALL_CLEAR:
            renderer.set_effects(effects)
            renderer.draw_game_screen(mouse_pos, restart_btn, game_home_btn,
                                      effects.blocked_cells(), hover_cell)
            renderer.draw_all_clear_screen(mouse_pos, all_home_btn)

        elif screen_mode == SCREEN_FAIL:
            renderer.set_effects(effects)
            renderer.draw_game_screen(mouse_pos, restart_btn, game_home_btn,
                                      effects.blocked_cells(), hover_cell)
            renderer.draw_fail_screen(mouse_pos, retry_btn, fail_home_btn)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    main()
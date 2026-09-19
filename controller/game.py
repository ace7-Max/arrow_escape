# controller/game.py
from enum import Enum
from config import MAX_MISTAKES
from model.board import Board
from model.rules import is_blocked, is_all_cleared, calc_arrow_count


class GameState(Enum):
    PLAYING = 'playing'
    WIN = 'win'
    FAIL = 'fail'


class Game:
    def __init__(self):
        self.board = Board()
        self.level = 1
        self.mistakes = 0
        self.state = GameState.PLAYING
        self.finished = False
        self.animations = []
        self.feedback = ''
        self.feedback_type = ''
        self.start_level(1)

    def start_level(self, level):
        self.level = level
        self.mistakes = 0
        self.state = GameState.PLAYING
        self.finished = False
        arrow_count = calc_arrow_count(level)
        self.board.place_random(arrow_count, level=level)
        self.feedback = '第 ' + str(level) + ' 关开始'
        self.feedback_type = 'info'
        self.animations.clear()

    def restart_level(self):
        self.start_level(self.level)

    def next_level(self):
        TOTAL_LEVELS = 6
        if self.level + 1 > TOTAL_LEVELS:
            self.finished = True
            self.state = GameState.WIN
            return
        self.start_level(self.level + 1)

    def click_cell(self, r, c):
        if self.state != GameState.PLAYING:
            return
        if self.board.is_empty(r, c):
            return
        cell = self.board.get(r, c)
        direction = cell['dir']
        if is_blocked(self.board, r, c, direction):
            self._on_blocked(r, c, direction)
        else:
            self._on_fly_out(r, c, direction)

    def _on_blocked(self, r, c, direction):
        self.mistakes += 1
        self.animations.append(('blocked', r, c, direction))
        self.feedback = '被挡住了！失误 ' + str(self.mistakes) + '/' + str(MAX_MISTAKES)
        self.feedback_type = 'fail'
        if self.mistakes >= MAX_MISTAKES:
            self.state = GameState.FAIL
            self.feedback = '失误已满，关卡失败！'
            self.feedback_type = 'fail'

    def _on_fly_out(self, r, c, direction):
        self.animations.append(('fly_out', r, c, direction))
        self.board.remove(r, c)
        self.feedback = '飞出！'
        self.feedback_type = 'success'
        if is_all_cleared(self.board):
            self.state = GameState.WIN
            self.feedback = '第 ' + str(self.level) + ' 关完成！'
            self.feedback_type = 'win'
            self.animations.append(('win',))

    def consume_animations(self):
        a = self.animations[:]
        self.animations.clear()
        return a
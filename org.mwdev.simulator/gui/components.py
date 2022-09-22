import numpy as np
import pygame
import time

class Board:

    def __init__(self, window, parent_width, parent_height, width, height):
        """
        :param window:
        :param parent_width:
        :param parent_height:
        :param width:
        :param height:
        """
        self.parent_width = parent_width
        self.parent_height = parent_height
        self.width = width
        self.height = height
        self.window = window
        parent_comparator = min(self.parent_width, self.parent_height)
        cell_comparator = max(self.width, self.height)
        self.cell_width = int(parent_comparator / cell_comparator)

        self.params = None

    def params(self):
        pass

    def render(self, board_model):
        for x in range(self.width):
            for y in range(self.height):
                snake = board_model[x, y, 0] == 1
                food = board_model[x, y, 1] == 1
                self.render_cell(pos=(x, y), snake=snake, food=food)

    def render_cell(self, pos, snake, food):
        """
        :param pos: top-left corner of cell
        :param snake:
        :param food:
        :return:
        """
        pos_x = pos[0] * self.cell_width
        pos_y = pos[1] * self.cell_width
        rect = pygame.Rect(pos_x, pos_y, self.cell_width, self.cell_width)
        cell_color = (255, 255, 255)
        border_color = (0, 0, 0)
        if snake:
            cell_color = (0, 255, 0)
        elif food:
            cell_color = (255, 0, 0)
        pygame.draw.rect(self.window, cell_color, rect=rect)
        pygame.draw.rect(self.window, border_color, rect=rect, width=4 if snake else 1)


class Label:

    def __init__(self, position, text="", size=12, font=None, color=(0, 0, 0), refresh_count=None, background=None,
                 anti_alias=False):
        """
        - Custom label class for rendering labels
        :param position:
        :param text:
        :param size:
        :param font:
        :param color:
        :param refresh_count:
        :param background:
        :param anti_alias:
        """
        self.font = font
        self.original_text = text
        self.text = text
        self.color = color
        self.size = size
        self.position = position
        self.background = background
        self.anti_alias = anti_alias
        self.refresh_count = refresh_count
        self.current_count = 0

        if font is None:
            self.font = pygame.font.Font(pygame.font.get_default_font(), self.size)

    def render(self, window, position=None):
        text = self.font.render(self.text, self.anti_alias, self.color, self.background)
        window.blit(text, self.position if position is None else position)

    def append_text(self, text, refresh_count=None, append_to_front=False):
        if refresh_count is not None:
            self.refresh_count = refresh_count
        if self.refresh_count is None or self.current_count >= self.refresh_count:
            self.text = self.original_text + text if not append_to_front else text + self.original_text
            self.current_count = 0
        else:
            self.current_count += 1

    def update_text(self, text, refresh_count=None):
        if refresh_count is not None:
            self.refresh_count = refresh_count
        if self.refresh_count is None or self.current_count >= self.refresh_count:
            self.original_text = text
            self.text = text
        else:
            self.current_count += 1


class TimedLabel(Label):

    def __init__(self, position, timeout: float, queue, text="", size=12, font=None, color=(0, 0, 0),
                 refresh_count=None, background=None,
                 anti_alias=False):
        """
        :param position: (x, y)
        :param timeout: number of seconds for the label to last
        :param text:
        :param size:
        :param font:
        :param color:
        :param refresh_count:
        :param background:
        :param anti_alias:
        """
        super().__init__(position=position, text=text, size=size, font=font, color=color, refresh_count=refresh_count,
                         background=background, anti_alias=anti_alias)
        self.time_created = time.time()
        self.timeout = timeout
        self.queue = queue

    def render(self, window, position=None):
        if (time.time() - self.time_created) < self.timeout:
            text = self.font.render(self.text, self.anti_alias, self.color, self.background)
            window.blit(text, self.position)
        else:
            self._remove_label()

    def _remove_label(self):
        self.queue.remove_label()


class TimedLabelQueue:

    def __init__(self, window):
        self.labels = []
        self.current_label = None
        self._is_label_showing = False
        self._window = window

    def remove_label(self):
        self.current_label = None
        if len(self.labels) != 0:
            self.current_label = self.labels.pop(0)

    def display_label(self, label, force=False):
        if force or len(self.labels) == 0:
            self.current_label = label
        else:
            self.labels.append(label)

    def render(self):
        if self.current_label is not None:
            self.current_label.render(self._window)
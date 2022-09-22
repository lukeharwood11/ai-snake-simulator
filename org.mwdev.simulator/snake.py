import numpy as np


class SnakeCell:

    def __init__(self, next_cell, position, head_cell=False) -> None:
        """
        A cell is a building block for the snake
        """
        self.head_cell = head_cell
        self.next_cell = next_cell
        self.tail = None
        self.current_position = position
        self.previous_position = None

    def shift(self):
        self.previous_position = self.current_position
        self.current_position = self.next_cell.previous_position
        if self.tail is not None:
            # meaning we have more cells after us to update
            self.tail.shift()

    def die(self):
        if self.tail is not None:
            self.tail.die()
        self.tail = None
        self.current_position = None
        self.previous_position = None
        self.next_cell = None
        self.head_cell = None

    def add_cell(self):
        """
        add another cell to the end of the snake
        :return:
        """
        if self.tail is None:
            # means this is the tail
            self.tail = SnakeCell(next_cell=self, position=self.previous_position)
        else:
            self.tail.add_cell()


class Snake:

    def __init__(self, start_pos, agent) -> None:
        self.head = SnakeCell(None, start_pos, head_cell=True)
        self.start_pos = start_pos
        self.agent = agent
        self.length = 1

    def eat(self):
        self.length += 1
        self.head.add_cell()

    def reset(self):
        self.length = 1
        self.head.die()
        self.head = SnakeCell(next_cell=None, position=self.start_pos, head_cell=True)

    def step(self, inputs, keys_pressed, wall_hit, food):
        """
        :return:
        """
        direction = self.agent.update(inputs, food, wall_hit, keys_pressed)
        if direction == 0:
            # left
            pass
        elif direction == 1:
            # up
            pass
        elif direction == 2:
            # right
            pass
        elif direction == 3:
            # down
            pass


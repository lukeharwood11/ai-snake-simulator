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

    def shift(self, board, direction=None):
        self.previous_position = self.current_position
        if self.head_cell:
            assert direction is not None, "Direction cannot be None for 'Head' SnakeCell"
            self.current_position = self.current_position + direction
        else:
            self.current_position = self.next_cell.previous_position
        # clear the position on the board where we were
        board[self.previous_position[0], self.previous_position[1]] = np.array([0, 0])
        # activate the position on the board where we are
        board[self.current_position[0], self.current_position[1]] = np.array([1, 0])
        if self.tail is not None:
            # meaning we have more cells after us to update
            self.tail.shift(board)

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

    def __init__(self, start_pos, agent, starting_direction=2) -> None:
        self.head = SnakeCell(None, start_pos, head_cell=True)
        self.start_pos = start_pos
        self.agent = agent
        self.length = 1
        self.current_direction = starting_direction  # default direction is right

    @staticmethod
    def get_direction(direction):
        """
        :param direction: 'left', 'right', 'up', 'down'
        :return: int representation
        """
        if direction == 'left':
            return 0
        if direction == 'up':
            return 1
        if direction == 'right':
            return 2
        if direction == 'down':
            return 3

    def eat(self):
        self.length += 1
        self.head.add_cell()

    def reset(self):
        length = self.length
        self.length = 1
        self.head.die()
        self.head = SnakeCell(next_cell=None, position=self.start_pos, head_cell=True)
        return length

    def update(self, board, inputs, keys_pressed, wall_hit, food):
        """
        :return:
        """
        direction = self.agent.update(inputs, food, wall_hit, keys_pressed)
        assert direction <= 3, "Direction {} out of bounds.".format(direction)
        self.current_direction = direction
        self.step(board, food)

    def step(self, board, food):
        x = 0
        y = 0
        if self.current_direction == 0:
            # go left
            x = -1
        if self.current_direction == 1:
            # go up
            y = -1
        if self.current_direction == 2:
            # go right
            x = 1
        if self.current_direction == 3:
            # go down
            y = 1
        self.head.shift(board, direction=np.array([x, y]))
        if food:
            self.eat()


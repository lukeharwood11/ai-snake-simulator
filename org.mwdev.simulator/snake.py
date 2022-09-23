import numpy as np
from _global import SNAKE_COLOR, FOOD_COLOR

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

    def check_for_collision(self, head_pos=None):
        assert self.head_cell or (head_pos is not None), "Head Position cannot be None for a non-head-cell"
        if self.head_cell:
            head_pos = self.current_position
        else:
            if np.all(head_pos == self.current_position):
                return True
        if self.tail is not None:
            # meaning we have more cells after us to update
            return self.tail.check_for_collision(head_pos=head_pos)
        else:
            return False

    def shift(self, board, direction=None):
        self.previous_position = self.current_position
        if self.head_cell:
            assert direction is not None, "Direction cannot be None for 'Head' SnakeCell"
            self.current_position = self.current_position + direction
        else:
            self.current_position = self.next_cell.previous_position

        if 0 > self.current_position[0] or self.current_position[0] >= board.shape[0] \
                or self.current_position[1] < 0 or self.current_position[1] >= board.shape[1]:
            # out of bounds, don't update...
            return
        # clear the position on the board where we were
        if self.previous_position[0] < board.shape[1] and self.previous_position[1] < board.shape[1]:
            board[self.previous_position[0], self.previous_position[1]] = 0
        # activate the position on the board where we are
        board[self.current_position[0], self.current_position[1]] = SNAKE_COLOR
        if self.tail is not None:
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

    def print(self):
        if self.head_cell:
            print("-0-")
        else:
            print("||")
        if self.tail is not None:
            self.tail.print()

class Snake:

    def __init__(self, start_pos, agent, starting_direction=2) -> None:
        self.head = SnakeCell(None, start_pos, head_cell=True)
        self.start_pos = start_pos
        self.agent = agent
        self.length = 1
        self.starting_direction = starting_direction
        self.current_direction = starting_direction  # default direction is right

        assert agent is not None, "Agent cannot be None"

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
        self.current_direction = self.starting_direction
        self.head = SnakeCell(next_cell=None, position=self.start_pos, head_cell=True)
        return length

    def update(self, board, inputs, keys_pressed, wall_hit, food):
        """
        :return:
        """
        snake_collision = self.head.check_for_collision()
        if snake_collision:
            print("Collision.")
        direction = self.agent.update(inputs, food, wall_hit or snake_collision, keys_pressed)
        # 4 = current direction
        assert direction <= 4, "Direction {} out of bounds.".format(direction)
        self.current_direction = direction if direction != 4 else self.current_direction
        self.step(board, food)
        return snake_collision

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
            print("Length:", self.length)


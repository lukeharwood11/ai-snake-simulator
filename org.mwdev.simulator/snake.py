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

    def shift(self, board, direction=None, positions=None):
        assert self.head_cell or (positions is not None), "Positions cannot be None for a non-head-cell"
        self.previous_position = self.current_position
        if self.head_cell:
            assert direction is not None, "Direction cannot be None for 'Head' SnakeCell"
            self.current_position = self.current_position + direction
            positions = [self.current_position]
        else:
            self.current_position = self.next_cell.previous_position
            positions.append(self.current_position)
        if 0 > self.current_position[0] or self.current_position[0] >= board.shape[0] \
                or self.current_position[1] < 0 or self.current_position[1] >= board.shape[1]:
            # out of bounds, don't update...
            return
        # clear the position on the board where we were
        board[self.previous_position[0], self.previous_position[1]] = np.array([0, 0])
        # activate the position on the board where we are
        board[self.current_position[0], self.current_position[1]] = np.array([1, 0])
        if self.tail is not None:
            # meaning we have more cells after us to update
            return self.tail.shift(board, positions=positions)
        else:
            return positions

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

    def check_collision(self, list):
        position_set.add(self.current_position)
        position_set.intersection()
        if self.tail is not None:
            return self.tail.check_collision(position_set)

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
        direction = self.agent.update(inputs, food, wall_hit, keys_pressed)
        # 4 = current direction
        assert direction <= 4, "Direction {} out of bounds.".format(direction)
        self.current_direction = direction if direction != 4 else self.current_direction
        return self.step(board, food)

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
        positions = self.head.shift(board, direction=np.array([x, y]))
        if food:
            self.eat()
        return positions


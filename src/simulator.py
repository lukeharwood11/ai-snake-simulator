from constants import FOOD_COLOR, SNAKE_COLOR
from gui.components import Board
from utils import calculate_fps
from snake import Snake
from time import time
import numpy as np
import pygame
import os
import logging

log = logging.getLogger(__name__)


class Simulator:

    def __init__(self, width, height, model, fps=2, caption="AI Snake Simulator"):
        pygame.init()
        self.model = model
        self.window = pygame.display.set_mode((width, height))
        self.caption = caption
        self.fps = fps
        self.clock = pygame.time.Clock()
        self.board = Board(
            self.window, width, height, self.model.width, self.model.height
        )

        self.calc_fps = 0
        self.current_timestamp = None

    def start(self):
        """
        main 'game-loop' for simulation
        :return: None
        """
        # - - - - - - - - - - - - - - - - - - - - - - - - - -
        run = True
        pygame.display.set_caption(self.caption)
        # - - - - - - - - - - - - - - - - - - - - - - - - - -
        while run:
            if self.fps is not None and run:
                self.clock.tick(self.fps)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    if self.model is not None:
                        self.model.handle_close_event()
                    break
            t = self.current_timestamp
            self.current_timestamp = time()
            if t is not None:
                self.calc_fps = calculate_fps(self.current_timestamp - t)
            keys_pressed = pygame.key.get_pressed()
            run = self.model.update_state(keys_pressed) or run
            self.model.print_current_state()
            self.update_display()

    def update_display(self):
        self.board.render(self.model.board)
        pygame.display.update()

    def paint_board(self):
        pass

    def paint_snake(self):
        pass

    def paint_food(self):
        pass


class InputFrame:

    def __init__(self, input_shape, m):
        """
        - Regulates sequencing the inputs (m) at a time
        """
        self.input_shape = input_shape
        self.m = m
        self.inputs = []

    def update(self, inputs):
        if len(self.inputs) == self.m:
            self.inputs.pop(0)
        self.inputs.append(inputs)

    def get_input(self):
        _inputs = self.inputs
        while len(_inputs) < self.m:
            _inputs.append(_inputs[-1])
        return np.concatenate(_inputs, axis=1)

    def clear(self):
        self.inputs.clear()


class SimulatorModel:

    def __init__(self, width, height, agent, max_iterations, debug=True):
        """
        Keeps track of simulation domain
        - Goal is to be able to run the simulator headless (without a GUI)
        """
        self.num_channels = 1
        self.input_shape = (width, height, self.num_channels)
        # public variables
        # width and height are in terms of how many cells across and upwards respectively
        self.board_width = (width, height)
        self.width = width
        self.height = height
        self.agent = agent
        # board consists of width, height, and one color channel
        self.board = np.zeros(self.input_shape)
        self.snake = self.initialize_snake()
        # always must have a position, if it is None, then the snake wins (game over)
        self.food = self.generate_food_position()  # position
        # stats
        self.high_score = 0
        self.max_iterations = max_iterations
        self.scores = []

        self._debug = debug
        # A queue holding the last 4 (m) states
        self.input_frame = InputFrame(input_shape=self.input_shape, m=4)
        self.iteration_num = 1

    def initialize_simulation(self):
        self.generate_board()

    def generate_board(self):
        pass

    def initialize_snake(self):
        """
        For now, just start in the upper right corner
        :return:
        """
        snake = Snake(
            start_pos=np.array([0, 0]),
            agent=self.agent,
            starting_direction=Snake.get_direction("right"),
        )
        self.board[snake.start_pos[0], snake.start_pos[1]] = SNAKE_COLOR
        return snake

    def generate_food_position(self):
        """
        place the food in a random location that the snake does not currently occupy
        :return:
        """
        # trial and error solution
        invalid = True
        x = 0
        y = 0
        invalid_count = 0
        while invalid:
            x = np.random.randint(0, self.width)
            y = np.random.randint(0, self.height)
            if self.board[x, y] == 0:
                invalid = False
            elif self._debug:
                invalid_count += 1
        self.board[x, y] = FOOD_COLOR
        return np.array([x, y])

    def update_state(self, keys_pressed):
        """
        Single step through the model
        :param keys_pressed:
        :return:
        """
        snake_pos = self.snake.head.current_position
        wall_hit = self.is_out_of_bounds(snake_pos)
        food = np.all(self.food == snake_pos)
        self.input_frame.update(self.board.copy())
        self.board[self.food[0], self.food[1]] = 0
        snake_hit = self.snake.update(
            self.board,
            inputs=self.input_frame.get_input(),
            keys_pressed=keys_pressed,
            wall_hit=wall_hit,
            food=food,
        )
        refresh_food_pos = wall_hit or food or snake_hit
        if wall_hit or snake_hit:
            self.reset()
        if refresh_food_pos:
            self.food = self.generate_food_position()
        # refresh the food_position
        self.board[self.food[0], self.food[1]] = FOOD_COLOR
        return self.iteration_num == self.max_iterations

    def reset(self):
        score = self.snake.reset()
        # clear the inputs to start fresh
        self.input_frame.clear()
        self.iteration_num += 1
        self.high_score = max(self.high_score, score)
        self.scores.append(score)
        self.board = np.zeros((self.width, self.height, 1))
        self.board[0, 0] = SNAKE_COLOR

    def start_headless_simulation(self):
        """
        WARNING - assumes that a GUI simulation is not being run
        :return:
        """
        log.info("Starting Headless Simulation...")
        run = True
        while run:
            run = not self.update_state(keys_pressed=None)
        log.info("Simulation end.")
        log.info("Saving Model...")
        self.handle_close_event()
        self.print_simulation_summary()

    def is_out_of_bounds(self, position):
        return (
            0 > position[0]
            or position[0] >= self.width
            or position[1] < 0
            or position[1] >= self.height
        )

    def print_current_state(self):
        """
        - For debugging
        """
        pass

    def print_simulation_summary(self):
        log.info("Simulation Summary:")
        log.info(
            "- Ran {} iterations.\n- Max Length: {}\n".format(
                self.iteration_num, self.high_score
            )
        )

    def handle_close_event(self):
        self.agent.save_model("latest.weights.h5")

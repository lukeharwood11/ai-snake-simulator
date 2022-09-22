import pygame
import numpy as np
import matplotlib.pyplot as plt
from time import time
from snake import Snake
from utils import calculate_fps
import os


class Simulator:

    def __init__(self, model, fps=60, caption="AI Snake Simulator"):
        pygame.init()
        self.model = model
        self.window = pygame.display.set_mode(self.model.screen_dims)
        self.caption = caption
        self.fps = fps
        self.clock = pygame.time.Clock()

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
            self.model.update_state(keys_pressed)
            self.update_display()

    def update_display(self):
        pass

    def paint_board(self):
        pass

    def paint_snake(self):
        pass

    def paint_food(self):
        pass


class SimulatorModel:

    def __init__(self, width, height, agent, debug=True):
        """
        Keeps track of simulation domain
        - Goal is to be able to run the simulator headless (without a GUI)
        """
        pygame.init()
        # public variables
        # width and height are in terms of how many cells across and upwards respectively
        self.board_width = (width, height)
        self.width = width
        self.height = height
        self.agent = agent
        # board consists of width, height, and categorical (snake/no-snake, fruit/no-fruit)
        self.board = np.zeros((width, height, 2))
        self.snake = self.initialize_snake()
        # always must have a position, if it is None, then the snake wins (game over)
        self.fruit = self.generate_fruit_position()  # position
        # private variables
        self._debug = debug

    def initialize_simulation(self):
        pass

    def generate_board(self):
        pass

    def initialize_snake(self):
        """
        For now, just start in the upper right corner
        :return:
        """
        return Snake(np.array([0, 0], self.agent, starting_direction=Snake.get_direction("right")))

    def generate_fruit_position(self):
        """
        place the fruit in a random location that the snake does not currently occupy
        :return:
        """
        return 0, 0

    def update_state(self, keys_pressed):
        """
        Single step through the model
        :param keys_pressed:
        :return:
        """
        snake_pos = self.snake.head.current_position
        wall_hit = self.is_out_of_bounds(snake_pos)
        food = self.fruit == snake_pos
        self.board[self.fruit[0], self.fruit[1]] = np.array([0, 0])
        self.snake.update(self.board, inputs=self.board, keys_pressed=keys_pressed, wall_hit=wall_hit, food=food)
        if food:
            self.fruit = self.generate_fruit_position()
        self.board[self.fruit[0], self.fruit[1]] = np.array([0, 1])


    def start_headless_simulation(self):
        """
        WARNING - assumes that a GUI simulation is not being run
        :return:
        """
        pass

    def is_out_of_bounds(self, position):
        return 0 > position[0] >= self.width or 0 > position[1] >= self.height

    def print_current_state(self):
        """
        - For debugging
        """
        pass

    def handle_close_event(self):
        self.agent.save_model(os.path.join("assets", "models"))


def main():

    # step 1 - create an Agent
    agent = None
    # step 2 - create a SimulatorModel
    model = SimulatorModel(100, 100, agent=agent, debug=True)
    # step 3 - create a Simulator
    simulator = Simulator(model, fps=60, caption="AI Snake Simulator")

    # final step - run the Simulator!
    simulator.start()


if __name__ == "__main__":
    main()

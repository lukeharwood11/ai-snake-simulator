from abc import ABC, abstractmethod
from pygame import K_UP, K_LEFT, K_RIGHT, K_DOWN


class Agent(ABC):

    def __init__(self, num_inputs, num_outputs):
        self.num_inputs = num_inputs
        self.num_outputs = num_outputs

    """
    - Abstract agent class
    """

    @abstractmethod
    def update(self, inputs, reward_collision=False, wall_collision=False, keys_pressed=None):
        """
        - Given input from the simulation make a decision
        :param wall_collision: whether the model collided with the wall
        :param reward_collision: whether the model collided with a reward (food)
        :param inputs: game board input as numpy 3D array
        :param keys_pressed: a map of pressed keys
        :return direction: int [0 - num_outputs)
        """
        pass

    @abstractmethod
    def save_model(self, path):
        """
        - Save the brain of the agent to some file (or don't)
        :param path: the path to the model
        :return: None
        """
        pass

    @abstractmethod
    def load_model(self, path):
        """
        - Load the brain of the agent from some file (or don't)
        :param path: the path to the model
        :return: None
        """
        pass


class DefaultAgent(Agent):

    def __init__(self, num_inputs, num_outputs):
        super().__init__(num_inputs, num_outputs)

    def update(self, inputs, reward_collision=False, wall_collision=False, keys_pressed=None):
        if keys_pressed[K_LEFT]:
            return 0
        if keys_pressed[K_UP]:
            return 1
        if keys_pressed[K_RIGHT]:
            return 2
        if keys_pressed[K_DOWN]:
            return 3
        return 4

    def save_model(self, path):
        pass

    def load_model(self, path):
        pass

import pygame
import numpy as np
import matplotlib.pyplot as plt
from time import time

class Simulator:
    
    def __init__(self, model):
        pygame.init()
        self.model = model
        self.window = pygame.display.set_mode(self.model.screen_dims)
    
    def start(self):
        pass
    
    def paint_board(self):
        pass
    
    def paint_snake(self):
        pass
    
    def paint_food(self):
        pass
    
class SimulatorModel:
    
    def __init__(self, width, height, debug=True):
        """
        Keeps track of simulation domain
        - Goal is to be able to run the simulator headless (without a GUI)
        """
        pygame.init()
        
    def initialize_simulation(self):
        pass

    def generate_board(self):
        pass
    
    def generate_snake(self):
        pass
    
    def generate_fruit_position(self):
        pass
    
    def print_current_state(self):
        """
        - For debugging
        """
        pass


def main():
    pass

if __name__ == "__main__":
    main()
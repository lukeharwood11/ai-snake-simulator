# AI Snake Simulator | Deep Q-Learning (DQN)

This repo provides a simulator for the snake game!

The current design allows anyone to be able to implement there own Agents to beat the game. Different simulators can also be built by inheriting from any base class provided in the project, such as the `SimulatorModel`, `Simulator`, `Agent`, etc.

Use the following pattern for initializing your simulation:
```
def main():

    # step 1 - create an Agent
    agent = DefaultAgent(0, 4)
    # step 2 - create a SimulatorModel
    model = SimulatorModel(25, 25, agent=agent, debug=True)
    # step 3 - create a Simulator
    simulator = Simulator(width=800, height=800, model=model, fps=10, caption="AI Snake Simulator")

    # final step - run the Simulator!
    simulator.start()
```

from agent import DefaultAgent
from qlearn import QLearningAgent
from simulator import SimulatorModel, Simulator
from constants import INPUT_SHAPE, NUM_OUTPUT, VIDEO_INPUT_SHAPE
import argparse
import logging

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

log.info("Starting AI Snake Simulator...")


def main(user: bool, headless: bool, model: str | None, training: bool):
    assert not (user and headless), "Cannot use both user and headless mode."
    # step 1 - create an Agent
    agent_map = {
        "user": DefaultAgent(INPUT_SHAPE, 4),
        "qlearn": QLearningAgent(
            alpha=0.01,
            alpha_decay=0.01,
            y=0.6,
            epsilon=0.98,
            input_shape=VIDEO_INPUT_SHAPE,
            num_actions=NUM_OUTPUT,
            batch_size=64,
            replay_mem_max=500,
            save_after=100,
            load_latest_model=False,
            training_model=training,
            model_path=model,
            train_each_step=False,
            debug=False,
        ),
    }
    agent = agent_map["user" if user else "qlearn"]
    # step 2 - create a SimulatorModel
    model = SimulatorModel(
        INPUT_SHAPE[0], INPUT_SHAPE[1], agent=agent, debug=True, max_iterations=500
    )
    agent.set_simulator(simulator=model)
    # step 3 - create a Simulator
    if not headless:
        simulator = Simulator(
            width=800, height=800, model=model, fps=10, caption="AI Snake Simulator"
        )
        simulator.start()
    else:
        model.start_headless_simulation()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="AI Snake Simulator")
    parser.add_argument(
        "--user",
        action="store_true",
        help="Use user agent",
        default=False,
    )
    parser.add_argument(
        "--headless",
        action="store_true",
        help="Run in headless mode",
        default=False,
    )
    parser.add_argument(
        "--model",
        help="The path to the model to use",
        default=None,
    )
    parser.add_argument(
        "--training",
        action="store_true",
        help="Whether to train the model",
        default=False,
    )
    args = parser.parse_args()
    main(args.user, args.headless, args.model, args.training)

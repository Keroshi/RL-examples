import os
import sys

import gymnasium as gym
from stable_baselines3.dqn.dqn import DQN


if "SUMO_HOME" in os.environ:
    tools = os.path.join(os.environ["SUMO_HOME"], "tools")
    sys.path.append(tools)
else:
    sys.exit("Please declare the environment variable 'SUMO_HOME'")
import traci

from sumo_rl import SumoEnvironment

# This fixes premature TraCI connection attempts
os.environ["SUMO_RL_SUMO_WAIT_TIME"] = "3"


if __name__ == "__main__":
    env = SumoEnvironment(
        net_file="/home/jay/RL-examples/SUMO-RL/inputs/single-intersection.net.xml",
        route_file="/home/jay/RL-examples/SUMO-RL/inputs/single-intersection-vhvh.rou.xml",
        single_agent=True,
        use_gui=True,
        num_seconds=5000,
        out_csv_name="SUMO-RL/outputs/2way-single-intersection/dqn",
    )

    model = DQN(
        env=env,
        policy="MlpPolicy",
        learning_rate=0.001,
        learning_starts=0,
        train_freq=1,
        target_update_interval=500,
        exploration_initial_eps=0.05,
        exploration_final_eps=0.01,
        verbose=2,
    )
    model.learn(total_timesteps=100000)
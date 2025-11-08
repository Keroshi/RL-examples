import os
import sys

# --- SUMO setup ---
if "SUMO_HOME" in os.environ:
    tools = os.path.join(os.environ["SUMO_HOME"], "tools")
    sys.path.append(tools)
else:
    sys.exit("Please declare the environment variable 'SUMO_HOME'")

import numpy as np
import pandas as pd
import ray
import traci
import supersuit as ss
from ray import tune
from ray.rllib.algorithms.ppo import PPOConfig
from ray.rllib.env.wrappers.pettingzoo_env import ParallelPettingZooEnv
from ray.tune.registry import register_env
import sumo_rl


def env_creator(_):
    """Create and wrap the SUMO multi-agent environment."""
    base_env = sumo_rl.parallel_env(
        net_file="/home/jay/SUMO_Example/map.net.xml",
        route_file="/home/jay/SUMO_Example/routes.rou.xml",
        out_csv_name="./outputs/nairobi_CBD/ppo",
        use_gui=False,
        num_seconds=800,
    )

    env = ss.pad_observations_v0(base_env)
    env = ss.pad_action_space_v0(env)

    return ParallelPettingZooEnv(env)


if __name__ == "__main__":
    ray.init()

    env_name = "nairobi_CBD"
    register_env(env_name, env_creator)

    config = (
        PPOConfig()
        .environment(env=env_name, disable_env_checking=True)
        .rollouts(num_rollout_workers=2, rollout_fragment_length='auto')
        .training(
            train_batch_size=512,
            lr=2e-5,
            gamma=0.95,
            lambda_=0.9,
            use_gae=True,
            clip_param=0.4,
            grad_clip=None,
            entropy_coeff=0.1,
            vf_loss_coeff=0.25,
            sgd_minibatch_size=64,
            num_sgd_iter=10,
        )
        .debugging(log_level="ERROR")
        .framework(framework="torch")
        .resources(num_gpus=int(os.environ.get("RLLIB_NUM_GPUS", "0")))
    )

    tune.run(
        "PPO",
        name="PPO",
        stop={"timesteps_total": 10_000},
        checkpoint_freq=10,
        local_dir=os.path.join(os.path.expanduser("~/ray_results"), env_name),
        config=config.to_dict(),
    )

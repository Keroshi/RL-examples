import traci

sumoBinary = "sumo"
sumoCmd = [sumoBinary, "-c", "/home/jay/RL-examples/SUMO-RL/inputs/configs/simple.sumocfg"]
traci.start(sumoCmd)

step = 0

try:
    while step < 10000:
        traci.simulationStep()
        step += 1
finally:
    traci.close()
    print("Simulation ended.")
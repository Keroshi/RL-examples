import traci

# Path to your SUMO configuration file
sumo_cfg = "/home/jay/SUMO_Example/simple.sumocfg"

# Start SUMO with TraCI
traci.start(["sumo", "-c", sumo_cfg])

step = 0
try:
    while step < 100:  # Run for 1000 simulation steps, or until no vehicles remain
        traci.simulationStep()  # Advance one step in the simulation
        tls_ids = traci.trafficlight.getIDList()
        vehicle_ids = traci.vehicle.getIDList()  # Get all vehicle IDs currently in the simulation

        for vid,tls in zip(vehicle_ids,tls_ids):
            phase = traci.trafficlight.getPhase(tls)
            pos = traci.vehicle.getPosition(vid)  # (x, y) position in meters
            print(f"Step {step}: Vehicle {vid} at position {pos}")
            print(f"Step {step}: Traffic Light {vid} is {phase}")

        step += 1

finally:
    traci.close()
    print("Simulation ended.")

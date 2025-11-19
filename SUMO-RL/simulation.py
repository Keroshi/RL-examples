import os
import traci

# Configuration
sumo_cfg = "/home/jay/RL-examples/SUMO-RL/inputs/configs/simple.sumocfg"
output_dir = "/home/jay/RL-examples/SUMO-RL/outputs/visualization_outs"
frames_dir = os.path.join(output_dir, "frames")

# Create frames directory if it doesn't exist
os.makedirs(frames_dir, exist_ok=True)

# Start SUMO-GUI with TraCI
sumoBinary = "sumo-gui"  # use "sumo" for headless
traci.start([sumoBinary, "-c", sumo_cfg])

frame_count = 0

# Step through simulation
while traci.simulation.getMinExpectedNumber() > 0:
    traci.simulationStep()

    # Capture screenshot from SUMO-GUI
    screenshot_path = os.path.join(frames_dir, f"frame_{frame_count:04d}.png")
    traci.gui.screenshot(viewID="View #0", filename=screenshot_path)

    frame_count += 1

# Close SUMO
traci.close()

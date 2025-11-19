import asyncio
import traci
import os
import sys
import traceback
import sumolib

# Helper to get vehicle data
def get_simulation_state():
    vehicle_list = traci.vehicle.getIDList()
    data = []
    
    for veh_id in vehicle_list:
        # Get raw X, Y position
        x, y = traci.vehicle.getPosition(veh_id)
        angle = traci.vehicle.getAngle(veh_id)
        type_id = traci.vehicle.getTypeID(veh_id)
        
        # CONVERT TO GEO-COORDINATES (Lat, Lon)
        # returns (lon, lat)
        lon, lat = traci.simulation.convertGeo(x, y)
        
        data.append({
            "id": veh_id,
            "lat": lat,
            "lon": lon,
            "angle": angle,
            "type": type_id
        })
    return data

async def run_simulation_loop(websocket):
    """
    Steps the simulation and sends data to the client.
    """
    # 1. Find a free port to avoid "Address already in use" errors
    port = sumolib.miscutils.getFreeSocketPort()
    
    sumo_binary = "sumo" # or "sumo-gui" if you want to see it pop up on the server
    sumo_cmd = [
        sumo_binary,
        "-c", "/home/jay/RL-examples/SUMO-RL/inputs/configs/simple.sumocfg", # Use Absolute Path
        "--step-length", "0.1",
        "--no-step-log", "true",      # Disable step logging to stdout
        "--no-warnings", "true",      # Disable warnings
        "--log", os.devnull,          # Send log to nowhere (Linux)
        # If you have output files defined in your .sumocfg, override them here:
        # "--tripinfo-output", "NUL", # Windows
        # "--tripinfo-output", "/dev/null", # Linux
    ]

    print(f"Attempting to start SUMO on port {port}...")

    try:
        # 2. Start SUMO with a specific port and label to avoid singleton conflicts
        traci.start(sumo_cmd, port=port, label="sim1")
        conn = traci.getConnection("sim1") # Get the specific connection

        step = 0
        while step < 3600:
            # Use the specific connection object 'conn' instead of global 'traci'
            conn.simulationStep()
            
            # Get vehicle data
            vehicle_list = conn.vehicle.getIDList()
            data = []
            for veh_id in vehicle_list:
                x, y = conn.vehicle.getPosition(veh_id)
                angle = conn.vehicle.getAngle(veh_id)
                type_id = conn.vehicle.getTypeID(veh_id)
                
                # Convert to Geo
                lon, lat = conn.simulation.convertGeo(x, y)
                
                data.append({
                    "id": veh_id,
                    "lat": lat,
                    "lon": lon,
                    "angle": angle,
                    "type": type_id
                })

            # Send to Frontend
            await websocket.send_json({
                "step": step,
                "vehicles": data
            })
            
            # Control speed
            await asyncio.sleep(0.1) 
            step += 1
            
    except traci.exceptions.FatalTraCIError:
        print("SUMO closed the connection (simulation ended or crashed).")
    except Exception:
        # 3. Print the FULL error so we know what's wrong
        print("--- SIMULATION ERROR ---")
        traceback.print_exc()
        print("------------------------")
    finally:
        # 4. Clean shutdown
        print("Cleaning up simulation...")
        try:
            # Try to close the specific connection
            traci.switch("sim1")
            traci.close()
        except:
            pass # It might already be closed
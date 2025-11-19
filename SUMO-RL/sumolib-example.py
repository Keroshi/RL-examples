import sumolib

net = sumolib.net.readNet("/home/jay/RL-examples/SUMO-RL/inputs/nets/map.net.xml")

tls_positions = []

for tls_id in net.getTrafficLights():  # always returns string IDs
    # Use TraCI later to get TLS state
    # For position, we can approximate using the first lane of edges pointing to this TLS
    # sumolib does not store lane info inside TLS
    tls_positions.append({"id": tls_id, "x": 0, "y": 0})  # placeholder


print(tls_positions)
import requests
import time
import os
import socket  # To get a unique node ID (hostname)

API_SERVER_URL = "http://host.docker.internal:5000/add_node"
NODE_ID = socket.gethostname()  # Unique node ID
CPU_CORES = int(os.getenv("CPU_CORES", 2))  # Default to 2 cores

def register_node():
    response = requests.post(API_SERVER_URL, json={"node_id": NODE_ID, "cpu_cores": CPU_CORES})
    if response.status_code == 201:
        print("Node registered successfully:", response.json())
    else:
        print("Failed to register node:", response.text)

if __name__ == "__main__":
    register_node()
    while True:
        time.sleep(10)  # Simulating node's periodic activity

import requests
import time
import os
import socket  # To get a unique node ID (hostname)

NODE_ID = socket.gethostname()  # Unique node ID
CPU_CORES = int(os.getenv("CPU_CORES", 2))  # Default to 2 cores

API_SERVER_BASE_URL = "http://host.docker.internal:5000"

def register_node():
    response = requests.post(f"{API_SERVER_BASE_URL}/add_node", json={"node_id": NODE_ID, "cpu_cores": CPU_CORES})
    if response.status_code == 201:
        print("Node registered successfully:", response.json())
    else:
        print("Failed to register node:", response.text)

def send_heartbeat():
    try:
        response = requests.post(f"{API_SERVER_BASE_URL}/heartbeat", json={"node_id": NODE_ID})
        if response.status_code == 200:
            print(f"Heartbeat sent from node {NODE_ID}")
        else:
            print(f"Failed to send heartbeat: {response.text}")
    except Exception as e:
        print("Error sending heartbeat:", e)

if __name__ == "__main__":
    register_node()
    while True:
        send_heartbeat()
        time.sleep(5)  # Send heartbeat every 5 seconds 
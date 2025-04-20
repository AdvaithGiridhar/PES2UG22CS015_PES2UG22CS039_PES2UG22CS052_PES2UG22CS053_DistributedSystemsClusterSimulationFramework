from flask import Flask, jsonify, request
from utils.cluster_state import (
    register_node, update_heartbeat, get_all_nodes,
    assign_pod_to_node, mark_node_unhealthy, get_all_pods
)
from health_monitor import monitor_nodes
import uuid
import time

app = Flask(__name__)
monitor_nodes()  # Start the monitor thread on API server start

@app.route('/')
def home():
    return "Welcome to the Distributed Systems Cluster Simulation API!"

@app.route('/add_node', methods=['POST'])
def add_node():
    data = request.json
    if not data or 'node_id' not in data or 'cpu_cores' not in data:
        return jsonify({"error": "Invalid request, node_id and cpu_cores required"}), 400

    register_node(data['node_id'], data['cpu_cores'])
    return jsonify({"message": "Node registered successfully", "node_id": data['node_id']}), 201

@app.route('/list_nodes', methods=['GET'])
def list_nodes():
    return jsonify(get_all_nodes())

@app.route("/heartbeat", methods=["POST"])
def heartbeat():
    data = request.get_json()
    if not data or 'node_id' not in data:
        return jsonify({"error": "node_id is required"}), 400
    update_heartbeat(data["node_id"], time.time())
    return {"status": "ok"}

@app.route('/launch_pod', methods=['POST'])
def launch_pod():
    data = request.json
    if not data or 'cpu' not in data:
        return jsonify({"error": "Missing required 'cpu' field"}), 400

    requested_cpu = data['cpu']
    algorithm = data.get('algorithm', 'first_fit').lower()
    pod_id = f"pod_{uuid.uuid4().hex[:8]}"

    nodes = get_all_nodes()
    eligible_nodes = {
        nid: info for nid, info in nodes.items()
        if info['status'] == 'healthy' and info['available_cores'] >= requested_cpu
    }

    if not eligible_nodes:
        return jsonify({"error": "No suitable node found"}), 400

    selected_node_id = None
    if algorithm == 'first_fit':
        for nid in eligible_nodes:
            selected_node_id = nid
            break
    elif algorithm == 'best_fit':
        selected_node_id = min(eligible_nodes, key=lambda nid: eligible_nodes[nid]['available_cores'])
    elif algorithm == 'worst_fit':
        selected_node_id = max(eligible_nodes, key=lambda nid: eligible_nodes[nid]['available_cores'])
    else:
        return jsonify({"error": f"Unknown algorithm: {algorithm}"}), 400

    assign_pod_to_node(pod_id, selected_node_id, requested_cpu)

    return jsonify({
        "message": f"Pod launched using {algorithm} algorithm",
        "pod_id": pod_id,
        "node_id": selected_node_id
    }), 200

@app.route('/check_health', methods=['GET'])
def check_node_health():
    nodes = get_all_nodes()
    current_time = time.time()
    timeout_seconds = 15

    result = {}
    for node_id, node_info in nodes.items():
        last_beat = node_info.get('last_heartbeat')
        if last_beat is None or (current_time - last_beat > timeout_seconds):
            mark_node_unhealthy(node_id)
            result[node_id] = 'unhealthy'
        else:
            result[node_id] = 'healthy'

    return jsonify(result), 200

@app.route('/list_pods', methods=['GET'])
def list_pods():
    pods = get_all_pods()
    response = []
    for pod_id, pod_info in pods.items():
        response.append({
            "pod_id": pod_id,
            "node_id": pod_info["node_id"],
            "cpu": pod_info["cpu"],
            "status": "running"
        })
    return jsonify(response), 200

if __name__ == '__main__':
    app.run(debug=True)
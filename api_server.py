from flask import Flask, jsonify, request

app = Flask(__name__)

# Sample in-memory node list
nodes = []

@app.route('/')
def home():
    return "Welcome to the Distributed Systems Cluster Simulation API!"

@app.route('/add_node', methods=['POST'])
def add_node():
    """Adds a new node with a given number of CPU cores"""
    data = request.json
    if not data or 'node_id' not in data or 'cpu_cores' not in data:
        return jsonify({"error": "Invalid request, node_id and cpu_cores required"}), 400
    
    node = {
        "node_id": data['node_id'],
        "cpu_cores": data['cpu_cores'],
        "status": "healthy"
    }
    nodes.append(node)
    return jsonify({"message": "Node added successfully", "node": node}), 201

@app.route('/list_nodes', methods=['GET'])
def list_nodes():
    """Lists all registered nodes"""
    return jsonify({"nodes": nodes})

@app.route('/health', methods=['GET'])
def health_check():
    """Health check for the API server"""
    return jsonify({"status": "API is running"}), 200

if __name__ == '__main__':
    app.run(debug=True)
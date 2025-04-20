# utils/cluster_state.py
from threading import Lock

nodes = {}
pods = {}
lock = Lock()

def register_node(node_id, cpu_cores):
    with lock:
        nodes[node_id] = {
            'cpu_cores': cpu_cores,
            'available_cores': cpu_cores,
            'pods': [],
            'last_heartbeat': None,
            'status': 'healthy'
        }

def update_heartbeat(node_id, time_now):
    with lock:
        if node_id in nodes:
            nodes[node_id]['last_heartbeat'] = time_now
            nodes[node_id]['status'] = 'healthy'

def get_all_nodes():
    with lock:
        return nodes.copy()

def get_all_pods():
    with lock:
        return pods.copy()

def mark_node_unhealthy(node_id):
    with lock:
        if node_id in nodes:
            nodes[node_id]['status'] = 'unhealthy'

def assign_pod_to_node(pod_id, node_id, cpu_required):
    with lock:
        if node_id in nodes and nodes[node_id]['available_cores'] >= cpu_required:
            nodes[node_id]['available_cores'] -= cpu_required
            nodes[node_id]['pods'].append(pod_id)
            pods[pod_id] = {
                'node_id': node_id,
                'cpu': cpu_required
            }
            return True
        return False

def remove_node(node_id):
    with lock:
        if node_id in nodes:
            return nodes.pop(node_id)

def get_pods_by_node(node_id):
    with lock:
        if node_id in nodes:
            return nodes[node_id]['pods'].copy()
        return []

def get_pod_cpu(pod_id):
    with lock:
        return pods.get(pod_id, {}).get('cpu')

def remove_pod(pod_id):
    with lock:
        if pod_id in pods:
            node_id = pods[pod_id]['node_id']
            cpu = pods[pod_id]['cpu']
            if node_id in nodes and pod_id in nodes[node_id]['pods']:
                nodes[node_id]['pods'].remove(pod_id)
                nodes[node_id]['available_cores'] += cpu
            del pods[pod_id]
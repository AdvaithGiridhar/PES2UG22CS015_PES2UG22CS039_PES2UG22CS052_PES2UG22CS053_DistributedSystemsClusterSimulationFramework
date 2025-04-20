# pod_scheduler.py
from utils.cluster_state import get_all_nodes

def schedule_pod(cpu_needed, strategy='first_fit'):
    nodes = get_all_nodes()
    candidates = [(id, data['available_cores']) for id, data in nodes.items() if data['status'] == 'healthy' and data['available_cores'] >= cpu_needed]
    if not candidates:
        return None

    if strategy == 'first_fit':
        return candidates[0][0]
    elif strategy == 'best_fit':
        return min(candidates, key=lambda x: x[1])[0]
    elif strategy == 'worst_fit':
        return max(candidates, key=lambda x: x[1])[0]
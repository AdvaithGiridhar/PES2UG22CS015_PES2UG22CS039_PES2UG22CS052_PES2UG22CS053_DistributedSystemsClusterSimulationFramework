# health_monitor.py
import time
import threading
from utils.cluster_state import (
    get_all_nodes, mark_node_unhealthy, get_pods_by_node,
    get_pod_cpu, remove_pod, assign_pod_to_node, get_all_pods
)

def monitor_nodes(interval=5, timeout=15):
    def monitor():
        while True:
            time.sleep(interval)
            nodes = get_all_nodes()
            current_time = time.time()

            for node_id, node in nodes.items():
                last_beat = node.get("last_heartbeat")
                if last_beat is None or (current_time - last_beat) > timeout:
                    if node["status"] != "unhealthy":
                        print(f"[HealthMonitor] Node {node_id} marked as UNHEALTHY")
                        mark_node_unhealthy(node_id)

                        # RESCHEDULE PODS
                        failed_pods = get_pods_by_node(node_id)
                        for pod_id in failed_pods:
                            cpu = get_pod_cpu(pod_id)
                            remove_pod(pod_id)

                            # Reschedule using First-Fit (you can make this configurable)
                            rescheduled = False
                            for tgt_node_id, tgt_info in get_all_nodes().items():
                                if tgt_info["status"] == "healthy" and tgt_info["available_cores"] >= cpu:
                                    success = assign_pod_to_node(pod_id, tgt_node_id, cpu)
                                    if success:
                                        print(f"[Rescheduler] Rescheduled {pod_id} to {tgt_node_id}")
                                        rescheduled = True
                                        break

                            if not rescheduled:
                                print(f"[Rescheduler] Failed to reschedule pod {pod_id}")

    threading.Thread(target=monitor, daemon=True).start()
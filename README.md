Project Title : "Distributed Systems Cluster Simulation Framework" 

Problem Statement:

Develop a lightweight, simulation-based distributed system that mimics core Kubernetes cluster management functionalities. 

The system will create a simplified yet comprehensive platform for demonstrating key distributed computing concepts

High Level Architecture

● Implement an API server that integrates key functionalities such as node management, pod scheduling, and health monitoring.

● Nodes periodically send health signals for themselves

● To simplify the assignment, the system consists of a CLI/Web Interface that communicates with an API Server (Central Control Unit), which manages the Cluster
Infrastructure composed of Nodes and Pods.

Key Deliverables

1. Node addition to cluster

2. Pod scheduling

3. Node health monitoring and failure recovery

4. Listing of Nodes in cluster along with their health status

Technology Stack
1. Docker (For Simulating Nodes)

2. Flask, Node.js, or any other programming language for implementing an API server.

3. First-Fit, Best- Fit, Worst-Fit scheduling algorithm for pod Scheduling.


Weekly Guidelines

1. Week 1 (15 M)

1. Implement API Server base implementation and Node Manager functionality.

2. Add a Node → Provide CPU cores to join the cluster (launch new container).


2. Week 2 (15 M)

1. Implement Pod Scheduler and Health Monitor with node heartbeat mechanism.

2. Launch a Pod → Request a pod with CPU system assigns it automatically (adds to node's pod ID array).

3. Week 3 (10 M)

1. List Nodes → See all nodes and their health status.

2. System testing and documentation. 

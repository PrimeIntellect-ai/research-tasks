You are acting as an AI assistant for a Machine Learning Engineer who is preparing training data for a Continuous-Time Graph Neural Network (CT-GNN).

The engineer has written a Go program to simulate the Kuramoto model (a system of coupled non-linear ODEs) on a given graph. The output of this simulation will be used as the ground-truth time-series data. However, the current numerical integrator is using a hardcoded, excessively large step size (`dt = 0.5`). Because some nodes in the network have a high degree, the system becomes stiff, and the explicit Euler integration diverges, producing `NaN` values.

Your task is to fix the simulation code so that it automatically adapts the step size based on the network topology, and then generate the correct training data.

Here are the details:
1. The network topology is provided as an edge list in `/home/user/graph.edges`. Each line contains two space-separated integers representing an undirected edge between two nodes.
2. The buggy Go simulation code is located at `/home/user/simulate.go`.
3. You need to modify `/home/user/simulate.go` so that the integration step size `dt` is no longer hardcoded. Instead, it must be calculated dynamically as: `dt = 0.1 / (K * max_degree)`, where `K` is the coupling constant (already defined in the code) and `max_degree` is the maximum degree of any node in the parsed graph.
4. Ensure the number of integration steps is updated to `int(T / dt)` so the simulation still runs for the exact total time `T`.
5. Run the fixed simulation. It should output the final phases of all nodes to `/home/user/final_phases.csv`. The format should be `node_id,final_phase`, one per line, sorted by `node_id`.

Ensure that the output file `/home/user/final_phases.csv` is generated successfully and contains no `NaN` or `Inf` values. Do not modify the initial conditions, the model equations, `K`, or `T`.
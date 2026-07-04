You are acting as a machine learning engineer who needs to generate synthetic training data for a Graph Neural Network (GNN). The model will predict diffusion dynamics over a network topology. 

I have placed a simple network edge list in `/home/user/graph.txt`. The file contains undirected edges, one per line, comma-separated (e.g., `0,1`). There are exactly 4 nodes (IDs 0 to 3).

Write a Go program located at `/home/user/generate_data.go` that does the following:
1. **Graph Algorithm & Laplacian**: Reads `/home/user/graph.txt` and constructs the unnormalized Graph Laplacian matrix $L = D - A$.
2. **ODE Numerical Solving**: Simulates the heat diffusion equation $du/dt = -L u$ over the graph using the Forward Euler method. 
   - Initial conditions $u(0)$: node 0 has a value of `10.0`, and all other nodes have `0.0`.
   - Time step: $\Delta t = 0.01$.
   - Number of steps: 1000 (so time $t$ goes from `0.00` to `10.00`).
3. **Analytical Validation**: After the simulation, the program must validate that the system has practically reached its analytical steady-state (for a connected graph, this is an equal distribution of the initial sum, so `2.5` per node). If any node's final value deviates from the analytical steady-state by more than `0.1`, the program should panic or exit with a non-zero status.
4. **Observational Data Reshaping**: The program must write the time-series data to a CSV file at `/home/user/training_data.csv`.
   - The CSV must have the exact header: `time,node0,node1,node2,node3`.
   - Each row should represent a simulation step (starting at $t=0$).
   - Float values must be formatted to 4 decimal places.

Once you have written the Go code, compile and run it to produce the dataset.
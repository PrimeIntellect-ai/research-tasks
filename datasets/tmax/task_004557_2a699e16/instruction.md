You are a machine learning engineer preparing synthetic training data for a Graph Neural Network (GNN). The GNN will predict the propagation time of signals across different polymer network topologies. 

Your task is to write and execute a Rust program that performs Monte Carlo simulations of a signal propagation model on several graphs, and outputs the resulting mean propagation times into an HDF5 file.

# Specifications

**1. Input Data**
You will be provided with a text file at `/home/user/networks.txt` (you need to assume it exists, but I will describe its format here). 
Each line corresponds to a network and is formatted as: `GraphID NumNodes Edges`
- `GraphID` is an integer (1-indexed, ascending).
- `NumNodes` is the number of nodes $N$ (nodes are zero-indexed, from $0$ to $N-1$).
- `Edges` is a semicolon-separated list of edges, where each edge is a comma-separated pair of node indices. The graph is undirected.
Example line: `1 4 0,1;1,2;2,3;3,0`

**2. Simulation Model (Discrete-time Susceptible-Infected Model)**
For each graph, you must simulate the following process:
- **Initial State ($t=0$):** Node $0$ is "Infected" (has the signal). All other nodes are "Susceptible".
- **Time Step Updates:** In each discrete time step ($t=1, 2, 3, \dots$), the signal spreads. For *every* edge connecting an Infected node to a Susceptible node (determined at the *start* of the time step), the Susceptible node becomes Infected with an independent probability $p = 0.3$. 
  - *Note:* If a Susceptible node is connected to $k$ Infected nodes at the start of the step, it faces $k$ independent infection rolls (probability of remaining uninfected is $(1 - 0.3)^k$).
  - Once a node is Infected, it remains Infected forever.
- **Termination:** The simulation stops at the exact time step $T$ when all $N$ nodes are Infected.

**3. Monte Carlo Estimation**
- For each graph, perform $M = 5,000$ independent simulations.
- Calculate the mean time to full infection, $\langle T \rangle$, across the 5,000 runs.

**4. Output Format**
- Write your results to an HDF5 file located at `/home/user/training_data.h5`.
- The HDF5 file must contain a single 1D dataset named `mean_times` at the root group (`/mean_times`).
- The dataset must contain 64-bit floating point numbers (`f64`), where the $i$-th element is the mean propagation time $\langle T \rangle$ for the graph with `GraphID` $i+1$.

**Requirements & Constraints:**
- Use **Rust** to implement the simulation and data writing. You should initialize a Cargo project (e.g., in `/home/user/gnn_data`).
- You may use standard crates like `rand` for the Monte Carlo randomness and `hdf5` for writing the output file. (Hint: you can use `features = ["hdf5-src"]` or similar in your `Cargo.toml` if you need to build the C-library from source without root privileges, or use the pre-installed system packages).
- Your code must be robust enough to handle the specified rules. 
- You do not have root access. 
- Run your Rust application so that the `/home/user/training_data.h5` file is generated. Ensure your final action leaves this file intact.
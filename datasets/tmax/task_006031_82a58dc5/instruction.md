You are helping a computational chemistry researcher analyze a molecular network model. Direct matrix factorisation of the transition matrix has been failing due to the network being composed of nearly disconnected clusters (leading to a near-singular Laplacian). 

To bypass this, the researcher needs you to implement an MCMC random walk approach in C to estimate the stationary distribution, and validate it against the exact analytical solution.

The molecular network is stored as an undirected edge list in `/home/user/network.txt`. Each line contains two integers representing an edge between two node IDs.

Your task is to write a C program at `/home/user/mcmc_graph.c` that does the following:
1. Parses `/home/user/network.txt` to build the graph in memory.
2. Calculates the **exact analytical stationary probability** of being at **Node ID 5**. For a simple random walk on an undirected, connected, non-bipartite graph, the analytical stationary probability of a node $v$ is $deg(v) / (2 \times |E|)$.
3. Performs an **MCMC random walk simulation** starting at Node ID 0 for exactly `1,000,000` steps. At each step, the walker should choose a uniformly random neighbor of the current node to transition to. Track the empirical frequency of visiting Node ID 5.
4. Writes the results to `/home/user/results.txt` strictly in the following format (rounding floats to 4 decimal places):
   ```
   Analytical: 0.XXXX
   MCMC: 0.XXXX
   ```

Compile your C program using `gcc -O3 -o /home/user/mcmc_graph /home/user/mcmc_graph.c` and run it to produce the `results.txt` file.
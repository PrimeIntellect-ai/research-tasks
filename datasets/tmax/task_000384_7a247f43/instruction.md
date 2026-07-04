You are acting as a research assistant for a systems biology lab. We are modeling the diffusion and decay of a chemical across a network of micro-bioreactors. 

The network topology is given as an adjacency matrix in `/home/user/graph.csv` (comma-separated, no headers, where `1` indicates a connection and `0` indicates no connection). 
The initial concentration of the chemical in each reactor at time $t=0$ is given in `/home/user/initial.csv` (one value per line, corresponding to the row index in the adjacency matrix).

You need to write a Python script at `/home/user/run_sim.py` that performs the following steps:

1. **Network ODE Simulation**:
   Construct the Graph Laplacian $L$ from the adjacency matrix $A$. The Laplacian is defined such that the off-diagonal entries are $L_{ij} = A_{ij}$ and the diagonal entries are $L_{ii} = -\sum_{j \neq i} A_{ij}$.
   Simulate the concentration $C$ in the reactors over time $t$ using the ODE system:
   $$\frac{dC}{dt} = D \cdot L \cdot C - \lambda \cdot C$$
   where the diffusion coefficient $D = 0.8$ and the decay constant $\lambda = 0.1$.
   Use `scipy.integrate.solve_ivp` to solve this system from $t = 0$ to $t = 5.0$. 

2. **Probability Distribution Metric**:
   Extract the final unnormalized concentrations of all nodes at exactly $t = 5.0$. 
   Convert this final state into a probability distribution $P$ by normalizing the vector so that it sums to 1.
   Compare $P$ to a discrete uniform distribution $Q$ (where $Q_i = 1/N$ for all $N$ nodes) by computing the Jensen-Shannon distance. Use `scipy.spatial.distance.jensenshannon` with base 2.

3. **Output**:
   - Write the Jensen-Shannon distance to `/home/user/js_distance.txt` rounded to exactly 6 decimal places.
   - Write the unnormalized concentration of node 0 at $t=5.0$ to `/home/user/node0_c.txt` rounded to exactly 6 decimal places.

Make sure your script executes successfully and generates the correct output files.
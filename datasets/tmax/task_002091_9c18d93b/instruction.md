You are a performance engineer profiling a new C++ inference application. The application calculates the stationary distribution of a network using two methods: an exact analytical solution via matrix decomposition, and an empirical estimation via Markov Chain Monte Carlo (MCMC) sampling.

Your task is to implement this application in C++ using the Eigen3 library for the exact solver.

Write a C++ program at `/home/user/pagerank.cpp` that does the following:
1. Reads an undirected graph from `/home/user/graph.txt`. The first line contains the number of nodes $N$. The remaining lines contain pairs of space-separated integers representing undirected edges between node `u` and node `v`.
2. Computes the exact PageRank stationary distribution. The PageRank equation is:
   $(I - d P^T) x = \frac{1-d}{N} \mathbf{1}$
   where $d = 0.85$ is the damping factor, $P$ is the transition matrix ($P_{ij} = 1/\text{deg}(i)$ if an edge exists between $i$ and $j$, and 0 otherwise), and $\mathbf{1}$ is a vector of ones. Use Eigen3's matrix decomposition features (e.g., LU decomposition) to solve this linear system for $x$.
3. Computes the empirical PageRank distribution using MCMC sampling. 
   - Start at node `0`.
   - Perform `10,000,000` steps.
   - At each step, generate a random uniform number $r \in [0, 1)$. If $r < 0.85$, move to a uniformly chosen neighbor of the current node. Otherwise (with probability $0.15$), jump to a uniformly chosen node in the entire graph (from $0$ to $N-1$).
   - Count the frequency of visits to each node to estimate the empirical probability distribution.
4. Output the results to a CSV file at `/home/user/results.csv` with the exact format:
   ```csv
   Node,Exact,Empirical
   0,0.1234,0.1235
   1,0.5678,0.5670
   ...
   ```
   Both `Exact` and `Empirical` values must be rounded to exactly 4 decimal places.

Compile your code using `g++ -O3 -I/usr/include/eigen3 pagerank.cpp -o pagerank` and run it to produce the `results.csv` file. Ensure your MCMC simulation runs enough steps to converge closely to the exact solution (the empirical values should match the exact values within a tolerance of $\pm 0.005$).
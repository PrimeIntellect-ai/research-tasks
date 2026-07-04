A researcher is studying diffusion on a specific spatial network and needs a C++ tool to analyze the random walk properties of the structure. 

You need to write a C++ program `/home/user/analyze_network.cpp` that models diffusion on an undirected network and extracts its macroscopic properties using Monte Carlo simulation, graph algorithms, curve fitting, and numerical integration.

The network edge list is located at `/home/user/graph.txt`. Each line contains two space-separated integers representing an undirected edge between two vertices. The vertices are numbered contiguously from 0 to N-1.

Your C++ program must perform the following steps:
1. Load the network from `/home/user/graph.txt` and represent it as an adjacency list. Sort the neighbors of each vertex in ascending order of their vertex IDs.
2. Use Breadth-First Search (BFS) to compute the shortest-path distance from the starting vertex `0` to all other vertices. If a vertex is unreachable, its distance is 0 for this exercise (though the provided graph is connected).
3. Perform a Monte Carlo simulation of `10,000` independent random walkers. 
   - Each walker starts at vertex `0` at time `t = 0`.
   - For each time step from `t = 1` to `t = 100`, the walker moves to a uniformly chosen random neighbor of its current vertex.
   - Use `std::mt19937` initialized with the seed `42` as your PRNG. To pick a random neighbor for a vertex with degree `D`, generate a random integer `k` in the range `[0, D-1]` using `std::uniform_int_distribution<int>(0, D - 1)`. The walker moves to the `k`-th neighbor in the sorted adjacency list. The PRNG should be created once and shared across all steps and walkers (simulate walker 1 for 100 steps, then walker 2 for 100 steps, etc.).
4. For each time step `t` in `[1, 100]`, calculate the Mean Squared Displacement `MSD(t)`. This is the average of the *squared shortest-path distance* (computed in step 2) from vertex `0` across all 10,000 walkers at time `t`.
5. The diffusion process typically follows $MSD(t) \approx C t^\alpha$. Find the anomalous diffusion exponent $\alpha$ by performing simple linear regression on the data points $(\ln t, \ln MSD(t))$ for $t \in [10, 100]$ inclusive. Calculate the slope of the best-fit line. Use the natural logarithm.
6. Compute the numerical integral of $MSD(t)$ with respect to $t$ from $t = 1$ to $t = 100$ using the standard trapezoidal rule with a step size of $\Delta t = 1$.
7. Output the results to `/home/user/results.txt` exactly in the following format (rounded to 3 decimal places):
```
Alpha: <value>
Integral: <value>
```

Ensure your C++ file compiles successfully with `g++ -O3 -std=c++17 analyze_network.cpp -o analyze_network` and run it to produce the `results.txt` file.
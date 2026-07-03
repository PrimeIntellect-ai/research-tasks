You are acting as a data scientist fitting a molecular interaction model. We have a graph representing a molecular network, and we want to evaluate how well a simple random walk model on this network approximates an experimentally observed activity distribution.

You need to write a Go program (`/home/user/mc_fit.go`) to perform a Monte Carlo simulation of a random walk on this graph and compute the Total Variation Distance (TVD) between the simulated visited-node distribution and the experimental distribution.

Here are the requirements:
1. Read the network graph from `/home/user/network.json`. The graph is an undirected adjacency list (map of string to array of strings).
2. Read the experimental distribution from `/home/user/experimental_dist.json` (map of string to float64 probabilities).
3. Implement a Monte Carlo random walk simulation:
   - Initialize the walk at node "A".
   - Keep a tally of visited nodes (including the starting node at step 0).
   - For `1,000,000` steps, randomly select a neighbor of the current node and move to it, incrementing the tally for the new node.
   - Use Go's `math/rand` with a fixed seed to ensure your simulation runs predictably, or rely on the Law of Large Numbers (1,000,000 steps will converge nicely). 
   - Ensure the neighbor selection is uniform. (Tip: Sort the neighbors alphabetically before selecting if your logic depends on indices, though uniform random selection on an unordered slice is mathematically equivalent).
4. Convert the final tallies (out of 1,000,001 total observations) into an empirical probability distribution.
5. Compute the Total Variation Distance (TVD) between your empirical distribution and the experimental distribution. The formula for TVD between distributions P and Q is: `0.5 * sum(|P(x) - Q(x)|)` for all nodes x.
6. Write the final TVD as a floating-point number rounded to 4 decimal places to `/home/user/tvd_result.txt`.

Run your Go program so that `/home/user/tvd_result.txt` is populated correctly.
You are a Machine Learning Engineer preparing structural features for a Graph Neural Network (GNN). You need to process a protein structure file, construct a spatial graph, estimate statistical properties, and run a Markov Chain Monte Carlo (MCMC) sampling process to identify central residues.

I have placed a PDB file at `/home/user/data/protein.pdb`. 

Write and execute a Python script to do the following:
1. **Bioinformatics Parsing:** Parse the PDB file and extract the 3D coordinates (x, y, z) of all alpha-carbon atoms (lines starting with `ATOM` where the atom name is exactly `CA`). Maintain their 0-based index order as they appear in the file.
2. **Graph Construction:** Create an undirected graph where each node represents a `CA` atom. Add an edge between any two nodes if the Euclidean distance between their coordinates is $\le 8.0$ Ångströms. Do not include self-loops.
3. **Bootstrap Confidence Intervals:** Calculate the degree of every node. Compute the mean node degree. Then, set the random seed via `numpy.random.seed(42)` and use bootstrapping with $B=1000$ resamples (sampling with replacement from the list of node degrees) to calculate the 95% confidence interval for the mean node degree. Use `numpy.percentile` with `[2.5, 97.5]` to find the lower and upper bounds.
4. **MCMC Sampling:** Keep the random state as is (do not re-seed). Perform a random walk (a simple MCMC sampling on the discrete state space of the graph nodes) for exactly 10,000 steps. 
    - Start the walk at node index `0`.
    - In each step, transition to a randomly and uniformly chosen neighbor of the current node using `numpy.random.choice`. (Assume the graph is fully connected; if a node were to have 0 neighbors, it would stay in place).
    - Tally the visit frequencies of all nodes during the 10,000 steps (including the starting position at step 0). Find the top 5 most frequently visited nodes. Break ties by favoring the smaller node index.
5. **Output:** Save the results to `/home/user/features.json` with exactly the following schema:
```json
{
  "num_nodes": int,
  "num_edges": int,
  "mean_degree": float,
  "ci_lower": float,
  "ci_upper": float,
  "top_5_mcmc_nodes": [int, int, int, int, int]
}
```

Ensure the output is properly formatted and all mathematical operations are implemented accurately. You may install any necessary Python packages (like `numpy`, `scipy`, or `networkx`) to complete the task.
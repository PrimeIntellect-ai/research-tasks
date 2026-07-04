You are a bioinformatics analyst tasked with developing a robust pipeline to assess the complexity of DNA sequences using De Bruijn graphs and probability distribution metrics. 

There are two main objectives to this task:

### Part 1: Fix the Environment
We process sequence graphs using the `networkx` library. For compliance and reproducibility, we vendor our dependencies. The source code for `networkx` version 2.8.8 has been vendored at `/app/networkx_src`. However, a recent configuration change broke its installation. 
1. Navigate to `/app/networkx_src`.
2. Identify and fix the deliberate typo in its configuration that prevents it from being installed.
3. Install the package locally into your python environment using `pip install /app/networkx_src`.

### Part 2: Sequence Graph Analyzer
You must write a Python script at `/home/user/sequence_graph_analyzer.py` that processes a single DNA sequence and computes a specific complexity metric based on the topology of its De Bruijn graph.

Your script must accept exactly one command-line argument (a string representing a DNA sequence containing only A, C, G, T) and print a single floating-point number to standard output.

**Algorithm Specifications:**
1. **Extract k-mers**: Extract all overlapping 3-mers (k=3) from the input DNA sequence. For example, the sequence `ACGCG` has the 3-mers `ACG`, `CGC`, and `GCG`.
2. **Build the De Bruijn Graph**: Construct a directed multigraph (using `networkx.MultiDiGraph`) where edges represent the 3-mers. For each 3-mer, add a directed edge from its length-2 prefix to its length-2 suffix. 
3. **Calculate Out-Degree Distribution**: 
   - Calculate the out-degree (number of outgoing edges) for every unique node present in the graph.
   - Count how many nodes have an out-degree of 0, 1, 2, 3, and 4. (Since the alphabet is A, C, G, T, a node can have at most 4 outgoing edges).
   - Create an empirical probability distribution vector `P` of length 5 by dividing these counts by the total number of unique nodes in the graph.
4. **Compute Distance Metric**:
   - We compare `P` against a theoretical reference distribution `Q` for a "complex" sequence, where `Q = [0.05, 0.25, 0.40, 0.25, 0.05]` (corresponding to out-degrees 0, 1, 2, 3, 4).
   - Calculate the Wasserstein-1 distance (Earth Mover's Distance) between the empirical distribution `P` and the reference distribution `Q`. Use `scipy.stats.wasserstein_distance` where the values are `[0, 1, 2, 3, 4]` and the weights are `P` and `Q` respectively.
5. **Output**: Print the computed Wasserstein distance formatted to exactly 6 decimal places (e.g., `0.350000`). Print nothing else.

**Example execution:**
```bash
python3 /home/user/sequence_graph_analyzer.py ACTGACTGACTG
```

Make sure your implementation is highly efficient and strict with the mathematical definitions.
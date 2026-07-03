You are a bioinformatics analyst working on understanding sequence motifs through graph theory. We want to analyze a De Bruijn-style k-mer graph of a specific DNA sequence and compute the steady-state importance of each k-mer using the PageRank algorithm. We also want to validate a custom iterative PageRank implementation against an analytical solution to test for convergence.

Here is the DNA sequence you must use for this analysis:
`AATGCGTAAGCTAGCTAGCATCGATCGATCGATCGAATCGCTAGCTAGCATCGA`

Your task is to write a Python script (and any necessary bash commands) to do the following:

1. **Graph Construction**:
   - Extract all contiguous 3-mers (k=3) from the sequence.
   - Construct a directed weighted graph where nodes are unique 3-mers.
   - A directed edge exists from node $X$ to node $Y$ if there is a 4-mer in the sequence where the prefix is $X$ and the suffix is $Y$ (i.e., they overlap by 2 characters).
   - The weight of the edge $X \rightarrow Y$ is the number of times this specific 4-mer appears in the sequence.
   - Normalize the edge weights so that the sum of weights for all outgoing edges from a node equals 1.0 (this forms the transition probability matrix $M$). If a node has no outgoing edges (a sink), it should transition equally to all nodes in the graph (including itself).

2. **Analytical Validation (Exact Solution)**:
   - Compute the exact PageRank vector $v_{exact}$ analytically. The PageRank equation is:
     $v = d M^T v + \frac{1-d}{N} \mathbf{1}$
     where $M^T$ is the transposed transition matrix, $d = 0.85$ is the damping factor, $N$ is the number of unique 3-mer nodes, $\mathbf{1}$ is a vector of ones, and $v$ is a column vector of probabilities summing to 1.
   - Solve for $v$ analytically: $v_{exact} = \frac{1-d}{N} (I - d M^T)^{-1} \mathbf{1}$

3. **Convergence Testing (Iterative Method)**:
   - Implement the Power Iteration method to compute PageRank iteratively:
     $v_{k+1} = d M^T v_k + \frac{1-d}{N} \mathbf{1}$
   - Start with an initial uniform probability vector $v_0 = [1/N, 1/N, ..., 1/N]^T$.
   - Run the power iteration. At iterations $k \in \{1, 5, 10, 20, 50\}$, calculate the $L_\infty$ norm (maximum absolute difference) between $v_k$ and $v_{exact}$.

4. **Visualization and Output**:
   - Generate a plot showing Iteration ($k$) on the x-axis and the $L_\infty$ error on the y-axis. Save this plot to `/home/user/convergence_plot.png`.
   - Save the computed $L_\infty$ errors to a JSON file at `/home/user/convergence.json`. The keys must be the iteration numbers as strings (`"1"`, `"5"`, `"10"`, `"20"`, `"50"`), and the values must be the floating-point error values.

**Constraints:**
- Ensure you work entirely within `/home/user`.
- You may use `numpy`, `scipy`, `networkx`, and `matplotlib`.
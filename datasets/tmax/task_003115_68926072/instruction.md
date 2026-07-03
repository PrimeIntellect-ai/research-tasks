You are a bioinformatics analyst tasked with building an overlap graph from a set of DNA sequences to study their connectivity distribution.

You have been provided with a FASTA file containing simulated DNA reads at `/home/user/sequences.fasta`.

Your objective is to write a Rust program that performs the following analysis:

1. **Overlap Graph Construction**:
   - Treat each sequence in the FASTA file as a node in a directed graph.
   - A directed edge exists from Node $i$ to Node $j$ (where $i \neq j$) if a suffix of sequence $i$ exactly matches a prefix of sequence $j$, and the match length is **at least 10 base pairs**.
   - If there are multiple valid overlap lengths between $i$ and $j$, only consider the longest one. The graph is unweighted, we just care about the existence of the edge.

2. **Degree Distribution Calculation**:
   - Calculate the **out-degree** of every node in the graph.
   - Compute the out-degree frequency distribution. That is, for each out-degree $x$, calculate $y$, which is the number of nodes that have exactly out-degree $x$.
   - Discard any out-degree $x$ where $y = 0$ (i.e., do not include points with zero frequency).

3. **Curve Fitting**:
   - We hypothesize that the out-degree distribution follows an exponential decay: $y = A e^{-bx}$.
   - Perform an Ordinary Least Squares (OLS) linear regression to fit the log-transformed data: $\ln(y) = \ln(A) - bx$. 
   - Note: The independent variable is $x$ (out-degree), and the dependent variable is $\ln(y)$. Solve for $\ln(A)$ (the intercept) and $-b$ (the slope), then calculate $A$ and $b$.

4. **Output Format**:
   - Create a JSON file at `/home/user/analysis_results.json` containing the following keys (all as numbers, with floats precise to at least 4 decimal places):
     - `"total_nodes"`: The number of sequences processed.
     - `"total_edges"`: The total number of directed edges in your overlap graph.
     - `"A"`: The calculated coefficient $A$ from the curve fitting.
     - `"b"`: The calculated coefficient $b$ from the curve fitting.

**Constraints & Rules**:
- You must write the solution in Rust. Create a Cargo project in `/home/user/sequence_graph`.
- You may use community crates (e.g., `serde`, `serde_json`) by adding them to your `Cargo.toml`.
- Do not modify the input FASTA file.
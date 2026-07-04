You are a machine learning engineer preparing graph training data. You need to process a raw observational log of network interactions, compute node centralities using a provided Bash/Awk toolkit, and solve a non-linear equation to derive a target feature for each node.

Your tasks are:

1. **Observational Data Reshaping**: 
   Read the raw text file `/data/network_logs.txt`. The file contains multi-line blocks like:
   ```
   Source: 1
   Target: 2
   Weight: 1.5
   ```
   Parse this file and reshape it into a standard CSV edge list at `/home/user/edges.csv` with the header `source,target,weight`.

2. **Fix the Vendored Package**:
   We use a vendored toolkit located at `/app/pagerank-awk-1.0` to compute node centralities. However, the toolkit has a mathematical bug. In `/app/pagerank-awk-1.0/pr.awk`, the PageRank base dampening value is calculated as `base = 1 - d` instead of properly dividing by the number of nodes `N` (i.e., `base = (1 - d) / N`). Fix this bug in the vendored package.

3. **Compute Centrality**:
   Run the fixed toolkit on your `edges.csv` file:
   `/app/pagerank-awk-1.0/run_pagerank.sh /home/user/edges.csv > /home/user/pageranks.csv`
   The output will have the format `node,pagerank`.

4. **Non-linear Equation Solving**:
   Write a Bash script at `/home/user/derive_features.sh` that reads `/home/user/pageranks.csv` and computes a derived feature `X` for each node. `X` is the real root of the non-linear equation:
   `X^3 + X - P = 0`
   where `P` is the node's PageRank. You can solve this using Newton-Raphson in `awk` or `bc` (iterate until the change in X is less than 1e-6).
   
   Your script should output the final training data to `/home/user/training_data.csv` with the header `Node,PageRank,Derived_X`. The rows must be sorted numerically by Node ID.

Ensure your derived features are highly accurate. An automated verifier will compute the Maximum Absolute Error (MAE) between your `Derived_X` values and the exact mathematical roots.
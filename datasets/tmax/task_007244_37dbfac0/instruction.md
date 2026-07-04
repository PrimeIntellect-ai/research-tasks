You are a bioinformatics analyst tasked with reconstructing a sequence from an alignment graph and determining its minimal folding energy state through continuous optimization. 

You have been provided with two files:
1. `/home/user/graph.json`: A directed acyclic graph representing possible sequence alignments. Each node contains a sequence chunk. Edges have weights representing alignment confidence.
2. `/home/user/energy.py`: A script containing a surrogate thermodynamic model `compute_energy(w, seq)` that evaluates the free energy of a sequence given a 3-element parameter vector `w`.

Your task involves three steps:
1. **Graph Algorithm**: Parse `/home/user/graph.json` and find the *longest* path (by sum of edge weights) from the node `"start"` to the node `"end"`. Concatenate the sequence chunks of the nodes along this path to form the assembled sequence.
2. **Numerical Stability**: The provided `compute_energy` function contains a naive, numerically unstable implementation of the partition function (`np.log(np.sum(np.exp(...)))`). During optimization, this will cause an `OverflowError` or yield `NaN`s. You must edit `/home/user/energy.py` to make this calculation numerically stable (e.g., using the log-sum-exp trick) without changing the mathematical definition of the function.
3. **Optimization**: Write a Python script at `/home/user/solve.py` that uses `scipy.optimize.minimize` (using the default solver or `L-BFGS-B`) to find the optimal weight vector `w` (an array of length 3) that minimizes the energy of your assembled sequence. Use an initial guess of `w = [0.0, 0.0, 0.0]`.

Finally, your script should save the results to `/home/user/result.json` in the following exact format:
```json
{
  "sequence": "YOUR_ASSEMBLED_SEQUENCE",
  "optimal_weights": [w0, w1, w2],
  "min_energy": 123.456
}
```
(Include `optimal_weights` as a list of three floats, and `min_energy` as a float).

You may install any standard Python scientific libraries you need (like `scipy`, `numpy`) using `pip`.
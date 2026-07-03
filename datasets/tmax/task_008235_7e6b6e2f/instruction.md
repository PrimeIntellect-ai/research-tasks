You are a data scientist fitting a network-based model to observed data using C++.

We have a sensor network of 50 nodes (numbered 0 to 49). The topology is given in `/home/user/graph.txt` as a list of undirected edges (one edge per line, space-separated node IDs). The observed signal at each node is given in `/home/user/y.txt` (one float per line, corresponding to nodes 0 through 49).

Your task is to write a C++ program that:
1. **Graph Matrix**: Constructs the unnormalized graph Laplacian $L = D - A$, where $A$ is the adjacency matrix and $D$ is the degree matrix.
2. **Matrix Decomposition**: Computes the eigendecomposition of $L$. Extract the eigenvectors corresponding to the 2nd and 3rd smallest eigenvalues (i.e., indices 1 and 2 if sorted ascending). Let this $50 \times 2$ matrix be $X$.
3. **Optimization**: Fits a linear model $y = X w$ to find weights $w \in \mathbb{R}^2$ minimizing the mean squared error $J(w) = \frac{1}{2N} \sum_{i=1}^N (x_i^T w - y_i)^2$. Use Gradient Descent with:
   - Initial weights: $w = [0.0, 0.0]^T$
   - Learning rate: $0.1$
   - Number of iterations: $1000$
4. **Bootstrap Confidence Intervals**: To quantify uncertainty, generate 1000 bootstrap samples.
   - Initialize a random number generator: `std::mt19937 gen(42);` and `std::uniform_int_distribution<int> dist(0, 49);`
   - For each bootstrap iteration, sample 50 indices with replacement using `dist(gen)`. 
   - Extract the sampled rows of $X$ and $y$.
   - Fit $w^*$ for this sample using the exact same Gradient Descent procedure (1000 iterations, lr=0.1, starting from [0,0]).
   - After 1000 bootstrap iterations, compute the 2.5th and 97.5th percentiles for both $w_0$ and $w_1$. (Sort the 1000 estimates and pick the values at index 25 and 975).

Output the final results (the original $w$ fitted on the full data, and the bootstrap bounds) to `/home/user/results.json` in exactly this format:
```json
{
  "w0": 1.2345,
  "w1": -0.5678,
  "w0_lower": 1.1000,
  "w0_upper": 1.3000,
  "w1_lower": -0.6000,
  "w1_upper": -0.4000
}
```

Constraints & Environment:
- Use the Eigen3 library for matrix operations (you may need to install `libeigen3-dev` and compile with `-I /usr/include/eigen3`).
- Write and execute your C++ code to generate the `results.json` file.
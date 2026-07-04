You are an AI assistant helping a computational biology researcher run molecular network simulations. We are trying to find the optimal node-specific diffusion rates for a biological network to match an experimentally observed target probability distribution.

First, you need to use our custom graph library, `libgraphopt`, which is provided as source code in `/app/libgraphopt-1.2.0`. However, a colleague tried to compile it recently and said the build is broken. You will need to identify the issue in the package (likely in the build configuration), fix it, and compile the library. The library compiles to a static archive `libgraphopt.a`.

Next, write a C++ program (e.g., `/home/user/optimize_network.cpp`) that does the following:
1. Links against the fixed `libgraphopt` to read the network topology from `/home/user/data/topology.txt` (an edge list).
2. Uses the HDF5 C++ API (the `libhdf5-dev` package is installed) to read two datasets from `/home/user/data/network_states.h5`:
   - `initial_dist`: A 1D array of $N$ double-precision floats.
   - `target_dist`: A 1D array of $N$ double-precision floats.
3. Implements a discrete-time diffusion simulation. The state of the network at time $t$ is a vector $x_t$. The initial state is $x_0 =$ `initial_dist`. The update rule for 10 steps ($t=0$ to $9$) is:
   $x_{t+1} = x_t + \text{diag}(\alpha) \cdot A \cdot x_t$
   Where $A$ is the adjacency matrix of the graph (loaded via `libgraphopt`), and $\alpha$ is an $N$-dimensional vector of diffusion rates (parameters to optimize).
4. After 10 steps, normalize $x_{10}$ so that its elements sum to 1.0 (to represent a valid probability distribution). Let's call this normalized vector $\hat{x}_{10}$.
5. Uses Gradient Descent (or another optimization algorithm of your choice) to find the optimal vector $\alpha \in [0, 0.1]^N$ that minimizes the Kullback-Leibler (KL) divergence between `target_dist` and $\hat{x}_{10}$:
   $D_{KL}(target \parallel \hat{x}_{10}) = \sum_{i=1}^N target_i \log\left(\frac{target_i}{\hat{x}_{10, i}}\right)$
   (Assume `target_dist` is already normalized and strictly positive).
6. Initializes the optimization with $\alpha_i = 0.05$ for all $i$.

Once you have found the optimized $\alpha$ vector, save it to `/home/user/solution_alphas.csv`. The file must contain exactly $N$ lines, with one double-precision float per line corresponding to the optimized diffusion rate of each node (node index 0 to $N-1$).

Your code should be compiled and run in the terminal. The automated verifier will read your `solution_alphas.csv`, run the forward model, and check the KL divergence of your output.
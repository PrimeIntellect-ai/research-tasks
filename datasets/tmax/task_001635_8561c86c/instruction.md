You are an AI assistant helping a computational physics researcher. 

The researcher has been using a compiled simulation tool located at `/app/simulate_network` (a stripped Linux binary). This binary simulates stochastic heat diffusion on an input graph with a hidden, time-dependent periodic heat source driving node `0`.

The governing Stochastic Differential Equation (SDE) modeled by the binary is:
$$ dx_i = - \sum_{j} L_{i,j} x_j dt + \sin(\omega t) \delta_{i,0} dt + \sigma dW_i $$
where:
* $L$ is the unnormalized graph Laplacian ($L = D - A$, where $D$ is the degree matrix and $A$ is the adjacency matrix).
* $\omega$ is an unknown, hardcoded driving frequency.
* $\sigma dW_i$ represents significant thermal noise (Wiener process).
* $\delta_{i,0}$ is the Kronecker delta (the source only affects node 0).

The binary uses a Forward Euler-Maruyama numerical integration scheme with a fixed time step $dt = 0.01$ for exactly $1000$ steps (from step `0` with $t=0$ up to step `999` with $t=9.99$). The initial conditions are $x_i(0) = 0$ for all nodes.

To run the binary, the syntax is:
`/app/simulate_network <input_graph.txt> <output_signal.csv>`
* `<input_graph.txt>` must be an edge list (one edge per line, two space-separated integers). Nodes must be contiguous integers starting from `0`.
* `<output_signal.csv>` will contain exactly 1000 rows, representing the simulated value of $x_0$ at each time step.

Because of the high noise $\sigma$ and chaotic floating-point reduction order across threads, a single run is highly non-reproducible and masks the underlying deterministic signal.

Your tasks:
1. **Analyze:** Create test graphs and run the binary multiple times (Monte Carlo sampling). Use spectral analysis (Fourier transforms / FFT) to average out the noise and accurately estimate the hidden driving frequency $\omega$ (rounded to 3 decimal places).
2. **Re-implement:** Write a clean, deterministic script in any language you choose at `/home/user/solve_expected.py` (or `.sh`, `.pl`, etc.) that computes the exact theoretical expected values $\mathbb{E}[x_i]$ for all nodes after exactly 1000 steps.
   * Your script must take two arguments: `<input_graph.txt>` and `<output_expected.csv>`.
   * It must perform Forward Euler integration of the exact expectation (i.e., the noise term $\sigma = 0$) using the same $dt=0.01$ and $1000$ steps.
   * It must use the $\omega$ you discovered.
   * The `<output_expected.csv>` must contain the final expected values (at step 1000) for all nodes, sorted by node index, one value per line.

We will test your script by running it against a secret validation graph and checking if your output matches the true expected values.
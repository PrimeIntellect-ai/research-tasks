You are acting as a data scientist running a parallel network diffusion experiment. You have been given an image containing the experimental configuration parameters. Your goal is to extract these parameters, simulate a diffusion process on a network across multiple parallel processes, save the results in a scientific format, visualize the convergence, and expose a REST API to query the results.

**Phase 1: Parameter Extraction**
An image of the experimental setup is located at `/app/experiment_params.png`. Read this image using OCR (e.g., Tesseract) to extract two key values:
- `K_BASE`: The base diffusion constant.
- `THRESHOLD`: The convergence threshold.
*(Note: The image contains plain text. Extract the numeric values for these two variables.)*

**Phase 2: Parallel Graph Simulation**
Write an MPI-enabled Python script (using `mpi4py`) that simulates heat diffusion on a network. The script must be run with 4 MPI processes.
1. **Network Topology**: Each MPI process must generate the exact same Watts-Strogatz small-world graph using `networkx`: $N=200$ nodes, $k=4$ nearest neighbors, rewiring probability $p=0.1$, and a random seed of $42$.
2. **Initial State**: For each node $i \in \{0, 1, \dots, 199\}$, its initial value is $x_i(0) = \sin(i)$ (using radians).
3. **Parallel Sweep**: Each MPI rank $r \in \{0, 1, 2, 3\}$ will simulate the process using a rank-specific diffusion constant: $K_r = K\_BASE + (r \times 0.01)$.
4. **Diffusion Rule**: In each discrete time step $t$, update all nodes synchronously using:
   $x_i(t+1) = x_i(t) + K_r \sum_{j \in \text{Neighbors}(i)} (x_j(t) - x_i(t))$
5. **Convergence Testing**: The simulation for rank $r$ halts when the maximum absolute change for any node between $t$ and $t+1$ is strictly less than `THRESHOLD`. Record the number of iterations $T_r$ required to converge.

**Phase 3: Scientific I/O and Visualization**
1. Have the root MPI process (Rank 0) gather the final converged node arrays and the iteration counts $T_r$ from all ranks.
2. Rank 0 must save these results to an HDF5 file at `/app/simulation_results.h5`. The file should contain a group called `results`, with subgroups for each rank (e.g., `rank_0`, `rank_1`, etc.). Inside each rank's subgroup, store the final node array as a dataset `final_state` and the iteration count as an attribute `iterations`.
3. Rank 0 must generate a line plot comparing the variance of the node values $\text{Var}(x(t))$ over time for all 4 ranks until they converge. Save this plot to `/app/convergence_plot.png`.

**Phase 4: Multi-Protocol Service**
Create and run a Python web server (e.g., Flask or FastAPI) listening on `127.0.0.1:8080`.
The server must load the HDF5 file and expose the following HTTP GET endpoint: `/api/status/<rank_id>` (where `<rank_id>` is 0, 1, 2, or 3).
- **Authentication**: The server MUST require an HTTP header `X-API-Key: netdiff-88` for all requests to this endpoint. If missing or incorrect, return a 401 Unauthorized.
- **Response**: Upon successful authentication, return a JSON response with the exact format:
  `{"rank": <int>, "iterations_to_converge": <int>, "k_used": <float>}`
  *(Make sure `k_used` matches the $K_r$ used for that rank, rounded to 3 decimal places).*

Leave the web server running in the background. Do not stop it.
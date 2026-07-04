You are an ML Engineer preparing training data from a structural network vibration experiment. We have recorded a video of 3 nodes (A, B, and C) vibrating under stress. The video is located at `/app/experiment.mp4` (10 seconds, 30 FPS). 

Your objective is to build a reproducible pipeline in Go that extracts the vibration frequencies, correlates them with the network's graph structure, estimates a physical stiffness parameter using MCMC, and serves the results via an HTTP API.

Here are the specific requirements:

1. **Signal Processing (FFT)**: 
   Extract the frames from `/app/experiment.mp4`. The video shows three distinct white squares on a black background representing the nodes. Their fixed bounding boxes (x, y, width, height) are:
   - Node A: (50, 50, 20, 20)
   - Node B: (150, 50, 20, 20)
   - Node C: (100, 150, 20, 20)
   Write Go code to compute the average pixel intensity (grayscale) for each bounding box across all frames to create 3 time-series signals. Apply a Discrete Fourier Transform (DFT/FFT) to each signal to find the dominant vibration frequency (in Hz) for each node. Ignore the DC component (0 Hz).

2. **Graph Algorithms**:
   The network topology is provided in `/app/graph.json` as an adjacency list. Parse this file and implement a graph algorithm in Go to find the shortest path distance (number of edges) between Node A and Node C. Also, calculate the degree (number of connected edges) for each node.

3. **MCMC Posterior Estimation**:
   The physical stiffness parameter $\theta$ dictates the relationship between a node's degree $d_i$ and its vibration frequency $f_i$. The model assumes: $f_i \sim \mathcal{N}(\theta \cdot d_i, \sigma^2)$, where $\sigma = 0.5$.
   Implement a Metropolis-Hastings MCMC sampler in Go to estimate the posterior distribution of $\theta$. 
   - Use a Uniform(0, 10) prior for $\theta$.
   - Run the chain for 10,000 iterations (discarding the first 1,000 as burn-in).
   - Calculate the posterior mean of $\theta$.

4. **API Service**:
   Wrap your reproducible pipeline into a Go web server. The server must:
   - Listen on `127.0.0.1:9090`.
   - Require an `Authorization` header with the exact value `Bearer ml-data-token-992` for all endpoints.
   - Serve the following `GET` endpoints (returning `application/json`):
     - `/api/v1/graph-distance`: Return the shortest path from A to C: `{"distance": <int>}`
     - `/api/v1/frequencies`: Return the dominant frequencies: `{"A": <float>, "B": <float>, "C": <float>}` (rounded to 1 decimal place).
     - `/api/v1/parameter`: Return the MCMC posterior mean of the stiffness parameter: `{"theta": <float>}` (rounded to 2 decimal places).

Keep your service running so the automated verifier can query it. Use standard Go libraries or well-known packages (like `gonum`) as needed.
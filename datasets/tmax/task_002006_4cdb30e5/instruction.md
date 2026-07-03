You are a performance engineer tasked with profiling and fixing a scientific computing pipeline. 

We have a video artefact located at `/app/simulation.mp4`. This video contains a 2D rendering of a molecular dynamic network over 300 frames. The network consists of 50 dark nodes (circles) moving against a white background, with a dynamically updating adjacency structure based on a spatial proximity threshold (distance < 30 pixels).

Currently, there is a Go pipeline located at `/home/user/pipeline/` consisting of `main.go`. This pipeline is supposed to:
1. Extract the frames from `/app/simulation.mp4` using `ffmpeg`.
2. Parse each frame to detect the 2D centroids of the 50 nodes.
3. Construct an adjacency matrix $A$ and the corresponding Graph Laplacian $L = D - A$.
4. Compute the pseudo-inverse of the Laplacian $L^{\dagger}$ to evaluate the average effective resistance of the network (a key molecular connectivity metric) for each frame.
5. Compute the empirical probability distribution of the pairwise Euclidean distances between all nodes, and calculate the discrete Kullback-Leibler (KL) divergence between the distance distribution of Frame 0 and Frame 299 (using 20 equal-width bins from 0 to 200 pixels).

**The Problems:**
1. **Numerical Instability:** The molecular graph occasionally fractures into disconnected components. When this happens, the Laplacian matrix becomes near-singular in a way that causes the current Cholesky/LU-based matrix factorization in the Go code to fail or produce NaNs. You must implement a robust fallback or regularization (e.g., eigenvalue thresholding or Tikhonov regularization with $\epsilon = 1e-6$) using the `gonum.org/v1/gonum` package so that the effective resistance can be computed continuously without crashing.
2. **Performance Bottleneck:** The current implementation processes frames sequentially and is extremely slow. You need to optimize the pipeline (e.g., via goroutines for frame processing, efficient memory allocation) so that the entire execution from video to final metric takes less than 5 seconds.
3. **Missing Statistical Logic:** The KL divergence calculation is currently incomplete. You need to implement the distance metric computation between the two distributions. Add a smoothing factor of $1e-9$ to empty bins to avoid division by zero or log(0) errors.

**Your Goal:**
1. Fix the numerical instability in `/home/user/pipeline/main.go`.
2. Implement the missing KL divergence comparison.
3. Optimize the Go code.
4. Compile your optimized binary to `/home/user/pipeline/analyzer`.

The binary should output a single JSON file to `/home/user/results.json` with the following exact structure:
```json
{
  "max_effective_resistance": 12.345,
  "kl_divergence_0_vs_299": 0.123,
  "runtime_seconds": 2.45
}
```
(`max_effective_resistance` is the maximum average effective resistance across all 300 frames).

We will verify your solution by running `/home/user/pipeline/analyzer` and checking the numerical accuracy of your `kl_divergence_0_vs_299` against the ground truth, as well as ensuring your execution speed meets the threshold.
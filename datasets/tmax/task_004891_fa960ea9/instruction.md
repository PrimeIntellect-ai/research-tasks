You are an ML engineer preparing graph-based training data for a molecular chemistry model. We have a legacy proprietary feature extraction tool located at `/app/matrix_oracle`. This tool takes an adjacency matrix and produces a dense embedding. Unfortunately, the tool crashes with a segmentation fault if the input matrix is near-singular (specifically, if the smallest eigenvalue of the graph Laplacian is exactly 0, which happens with disconnected graphs).

Your task is to build a robust Python HTTP data preprocessing service that wraps this legacy tool, regularizes the input using Monte Carlo methods, and serves the sanitized features to our training pipeline.

Here are the requirements for your service:
1. **API Server:** Create a Python HTTP web service listening on `127.0.0.1:8000`. It must require an authorization header exactly matching: `Authorization: Bearer graph-token-999`.
2. **Endpoint:** Implement a `POST /extract` endpoint that accepts JSON data in the format: `{"num_nodes": N, "edges": [[u, v], ...]}` representing an undirected graph.
3. **Graph Regularization (Graph & Monte Carlo):** 
   - Convert the graph to a normalized adjacency matrix.
   - To ensure the graph is fully connected (avoiding the near-singular Laplacian crash in the oracle), add synthetic edges. You must simulate 5000 independent random walks of length 10 starting from random nodes. Add an edge of weight `0.01` between the start and end node of every walk.
   - **Parallelism Requirement:** The random walk simulation *must* be parallelized using Python's `multiprocessing` module across at least 4 processes.
4. **Oracle Interaction:** Save the regularized adjacency matrix to a temporary CSV file (no headers, comma-separated, `N` rows and `N` columns). Execute `/app/matrix_oracle <path_to_csv>`. The binary will print a list of `N` float values to standard output. Parse this embedding.
5. **Distance Metric:** Calculate the Total Variation (TV) distance between the steady-state distribution of your simulated random walks (the frequency of end nodes) and a uniform distribution `(1/N)`.
6. **Response:** Return a JSON response with status 200:
   `{"embedding": [float, float, ...], "tv_distance": float}`

Write, run, and leave this server running in the background. Do not exit your final script, so the verification system can query `127.0.0.1:8000/extract`.
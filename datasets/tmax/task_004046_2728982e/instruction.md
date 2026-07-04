You are an ML engineer preparing a data-loading service for a new distributed training pipeline. The pipeline ingests scientific data from HDF5 files, computes a global normalization factor (solving a simple linear scaling equation: `sum(features) * scale_factor = 1.0`), and serves the normalized features via HTTP.

We are using a proprietary third-party package for this, which has been vendored into your environment at `/app/ml-server-0.8.2`. 

Unfortunately, this package has two major issues:
1. **Non-reproducible floating-point reduction:** The script `/app/ml-server-0.8.2/compute_norm.sh` splits the HDF5 array extraction into parallel chunks and accumulates the sums. Due to the unpredictable order of parallel execution and the non-associative nature of floating-point arithmetic, the total sum (and thus the `scale_factor`) fluctuates slightly between runs. This non-determinism is ruining our model convergence. 
2. **Broken server configuration:** The Bash-based HTTP server wrapper `/app/ml-server-0.8.2/serve.sh` has a syntax error or logic flaw introduced during a recent patch, preventing it from binding and responding correctly.

Your task:
1. Investigate and fix the vendored package in `/app/ml-server-0.8.2` so that the feature sum is perfectly deterministic (e.g., by ensuring sequential/ordered accumulation of the chunked floating-point values before the final sum).
2. Fix the broken HTTP server script `serve.sh`.
3. Start the service. It must listen on `127.0.0.1:8080`.
4. The service must accept HTTP GET requests to the `/features` endpoint.
5. The service must require an authentication header: `X-Auth: secret-token-123`. If missing or incorrect, it should silently drop or return 403.
6. When queried correctly, it must process `/home/user/raw_input.h5` (dataset `/data/batch_1`), and return a valid HTTP 200 response with a JSON payload in this exact format:
   `{"scale_factor": 0.123456, "normalized_preview": [0.01, 0.02, 0.03]}` (where preview is the first 3 normalized values).

You must leave the service running in the background on port 8080 so the automated verifier can query it.
You are acting as an ML engineer preparing a real-time training data pipeline for a protein spectroscopy model. We have a multi-service setup located in `/app/` that needs to be fixed, integrated, and extended.

The system consists of three services:
1. **Raw Data Server**: A simple Python HTTP server running on `127.0.0.1:8080` that serves PDB (Protein Data Bank) files from `/app/data/`.
2. **Task Queue**: A Redis server running on `127.0.0.1:6379`.
3. **Data Prep API Server**: A Go service that you must implement. It should listen on `127.0.0.1:9000`.

**Your objective:**
Implement the Go Data Prep API Server in `/home/user/pipeline/main.go`. You need to bring up the Redis service and the Python file server using the provided scripts in `/app/scripts/`, and then run your Go API server.

**API Requirements:**
Your Go server must implement a REST API endpoint: `POST /prepare_training_data`.
The endpoint will receive a JSON payload: `{"pdb_id": "1XYZ", "num_bootstrap_samples": 1000}`.

When this endpoint is hit, your Go server must:
1. Fetch the corresponding PDB file (`http://127.0.0.1:8080/1XYZ.pdb`).
2. Parse the PDB file to extract all Alpha Carbon (CA) atom coordinates.
3. Simulate a pseudo-spectroscopy signal: calculate the Euclidean distance between consecutive CA atoms. These distances form a 1D signal sequence.
4. Apply a simple moving average filter of window size 3 to this 1D signal (padding with the first/last values for edges).
5. Compute the mean of the smoothed signal.
6. Calculate the 95% Bootstrap Confidence Interval for the mean of the smoothed signal using the requested number of bootstrap samples (resampling with replacement).
7. Cache the resulting calculated CI `[lower_bound, upper_bound]` in Redis with the key `spectro_ci_{pdb_id}`.
8. Return the JSON response: `{"status": "success", "mean": <float>, "ci_lower": <float>, "ci_upper": <float>}`.

Ensure your API requires a Bearer token for authentication: `Authorization: Bearer ml_prep_token_2024`. Requests without this token must return a 401 Unauthorized status.

Create a bash script at `/home/user/start_all.sh` that starts all three services in the background. Write your Go code using standard parallel computation practices (goroutines) where appropriate for the bootstrap sampling to make it efficient.
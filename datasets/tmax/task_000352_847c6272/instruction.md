You are a Data Engineer building an ETL and inference pipeline for a recommendation system. You need to implement a similarity search API, benchmark its performance under different numerical library configurations, and statistically analyze the results.

Here is your task:

1. **Similarity Search API**:
   You have a pre-generated feature matrix located at `/home/user/vectors.npy` (a NumPy array of shape 5000x100, dtype float32). 
   Write a Python web service (using Flask or FastAPI) in `/home/user/api.py` that listens on `127.0.0.1:8000`. 
   It must expose a `POST /search` endpoint that accepts a JSON payload containing a query vector: `{"query": [float, float, ...]}` (list of 100 floats).
   The endpoint must compute the cosine similarity between the query vector and all vectors in `/home/user/vectors.npy`, and return the indices of the top 5 most similar vectors (highest cosine similarity) in the format: `{"top_indices": [int, int, int, int, int]}`.

2. **Benchmarking Pipeline**:
   Write a Bash script `/home/user/benchmark.sh` that does the following:
   - Starts the `api.py` service with the environment variable `OMP_NUM_THREADS=1`.
   - Waits for the service to be ready.
   - Generates a synthetic query (100 random floats) and sends 200 sequential requests to the `/search` endpoint, recording the latency (response time) of each request.
   - Shuts down the service.
   - Repeats the entire process but with the service started using `OMP_NUM_THREADS=4`.
   - Saves the raw latency arrays (in milliseconds or seconds) to two files: `/home/user/latencies_1.txt` and `/home/user/latencies_4.txt` (one latency float per line).

3. **Statistical Analysis**:
   Write a Python script `/home/user/analyze.py` that reads the two latency files.
   It must perform a two-sided Welch's t-test comparing the means of the two latency distributions.
   It must calculate the 95% Confidence Interval for the difference between the means (`mean(threads=1) - mean(threads=4)`).
   Finally, it must output a JSON file at `/home/user/results.json` with exactly these keys:
   - `"mean_1"`: float (mean latency for 1 thread)
   - `"mean_4"`: float (mean latency for 4 threads)
   - `"p_value"`: float (p-value from the Welch's t-test)
   - `"ci_lower"`: float (lower bound of 95% CI for the difference)
   - `"ci_upper"`: float (upper bound of 95% CI for the difference)
   - `"significant"`: boolean (true if p-value < 0.05, false otherwise)

Constraints:
- Use standard Python libraries (`numpy`, `scipy`, `flask`/`fastapi`, `requests`, etc.). You may install them via pip if needed.
- Ensure the API computes cosine similarity correctly: `(A dot B) / (||A|| * ||B||)`.
- Your bash script `benchmark.sh` must be executable (`chmod +x`).
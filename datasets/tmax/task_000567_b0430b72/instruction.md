You are an MLOps engineer responsible for the integrity of experiment tracking artifacts. Our machine learning pipelines output artifact metrics (JSON files containing arrays of gradient norms, loss values, and validation scores) that are logged to a central tracking system. Recently, numerical instability (NaNs, extreme spikes) and corrupted logs have polluted our tracking database.

We have a multi-service tracking backend located in `/app/tracking_system/`:
1. A Redis cache that temporarily holds metrics.
2. A Flask API that receives metrics and writes them to Redis.
3. An Nginx reverse proxy that routes traffic to the Flask API.

Your task is twofold:

**Part 1: Service Composition & Configuration**
The services in `/app/tracking_system/` are currently misconfigured. You need to fix the configurations and glue them together so that an end-to-end flow works:
- Start the Redis server.
- Start the Flask app (ensure it connects to the local Redis instance on its default port).
- Configure Nginx to listen on port 8080 and reverse-proxy requests to the Flask app running on port 5000.
- Ensure all services are running and Nginx successfully accepts `POST /api/artifacts` requests.

**Part 2: Artifact Anomaly Detector (Rust)**
Write a Rust CLI application located at `/home/user/artifact_filter/target/release/artifact_filter` that reads a JSON file path as its first argument and determines if the artifact is "clean" or "corrupted/anomalous". 

The JSON files contain keys: `"gradient_norms"` (array of floats), `"loss_values"` (array of floats), and `"missing_ratio"` (float).
Your Rust program must perform the following:
1. **Missing Value & Outlier Handling:** Reject the artifact if `"missing_ratio"` > 0.05 or if any array contains `NaN` or `Infinity`.
2. **Sampling & Bootstrap Methods:** For the `"loss_values"`, take 100 random bootstrap samples (with replacement) of size `N/2` (where `N` is the length of the array). Calculate the mean of each sample. If the 95% confidence interval (2.5th to 97.5th percentile of the bootstrap means) spans a range greater than 50.0, reject the artifact as too unstable.
3. **Numerical Accuracy:** Reject the artifact if the sum of `"gradient_norms"` exceeds 1e5.

If the file is valid, the program must exit with code 0 and print `ACCEPT`.
If the file is anomalous, the program must exit with code 1 and print `REJECT`.

Configure your Rust project using appropriate numerical and JSON libraries (e.g., `serde`, `serde_json`, `rand`). Build it in release mode. 

Once your Rust tool is built, update the Flask app (`/app/tracking_system/app.py`) to invoke your Rust CLI via `subprocess` for every incoming JSON payload *before* saving it to Redis. If the Rust tool rejects it, the Flask API should return a `406 Not Acceptable`.

Create a log file at `/home/user/system_status.log` containing the text `READY` when you have completed all setup, compilation, and integration.
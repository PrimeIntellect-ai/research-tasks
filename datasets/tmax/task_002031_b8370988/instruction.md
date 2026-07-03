You are assisting a researcher organizing experimental datasets from multiple sensors. The researcher's streaming data pipeline is broken, and noisy, statistically anomalous data is polluting downstream analyses.

You need to write a statistical filter and fix the multi-service data pipeline.

**Part 1: Implement the Data Filter**
Create a Python script at `/home/user/filter.py`. The script will be invoked with a single command-line argument: the path to a JSON file containing sensor data.
- The JSON file contains an array of records: `[{"sensor_id": "S1", "timestamp": 1620000000, "value": 12.4}, ...]`.
- You must join this incoming data with the reference baselines located at `/app/reference_baselines.csv` (which has columns `sensor_id`, `baseline_mean`).
- For each `sensor_id` present in the JSON file, perform a 1-sample two-sided T-test (using `scipy.stats.ttest_1samp`) to test if the mean of the `value`s in the JSON file differs significantly from the `baseline_mean` for that sensor.
- Rules:
  - If a `sensor_id` in the JSON is missing from the reference baselines, immediately flag the file as anomalous.
  - If a `sensor_id` has fewer than 2 data points, you cannot perform the t-test; consider that specific sensor's data valid (do not flag it).
  - If the T-test p-value for ANY `sensor_id` is strictly less than 0.01, flag the file as anomalous.
- If the file is anomalous, print exactly `EVIL` to standard output and exit with status code `1`.
- If the file is valid, print exactly `CLEAN` to standard output and exit with status code `0`.

**Part 2: Reconfigure and Start the Pipeline Services**
The pipeline consists of three services:
1. An Nginx API gateway.
2. A Flask data ingestion application.
3. A Redis cache.

The configuration is currently incomplete. You must:
- Edit `/app/nginx/nginx.conf` so that HTTP requests arriving on port 8080 are reverse-proxied to the Flask app running on `127.0.0.1:5000`.
- Edit `/app/data_app/.env` and set the following variables:
  - `REDIS_HOST=127.0.0.1`
  - `REDIS_PORT=6379`
  - `FILTER_SCRIPT=/home/user/filter.py`
- Start the services by running the provided script: `bash /app/start.sh`.

Ensure that the services are running and that sending a JSON payload to `http://127.0.0.1:8080/upload` successfully triggers the pipeline.
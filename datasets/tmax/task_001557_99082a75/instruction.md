You are an operations engineer triaging an ongoing incident in our sensor data pipeline. The pipeline consists of three services: a Redis broker, a FastAPI sensor simulator, and a Python worker process that aggregates sensor readings. 

We are currently facing three critical issues:
1. **Accidental Deletion**: An engineer accidentally deleted the worker's configuration file (`config.json`). Fortunately, we have a raw dump of the partition it was on located at `/app/data/partition.img`. You need to recover the `config.json` file from this ext4 image and place it in `/app/worker/`.
2. **Worker Crash**: The worker script (`/app/worker/aggregator.py`) keeps crashing due to an `IndexError` when processing the batches. This looks like an off-by-one boundary condition in the batch window logic. You must debug and fix the script.
3. **Accuracy Drift**: The aggregated total values being written to `/app/worker/output/totals.csv` are failing our quality checks. Due to the way the sensor simulator generates tiny floating-point numbers, the worker's naive summation is losing precision. You need to repair the floating-point aggregation logic in the worker so that the accumulated totals have high precision.

Once you have recovered the config file and fixed the code, start the pipeline using the provided startup script: `/app/start.sh`. This script will launch Redis (port 6379), the FastAPI simulator (port 8000), and your fixed worker.

Let the pipeline run for 30 seconds so it can process the incoming batches. Then stop the services using `/app/stop.sh`.

The automated verifier will check the mean squared error (MSE) of the totals in `/app/worker/output/totals.csv` compared to a high-precision reference.
Your goal is to achieve an MSE of less than 1e-10.
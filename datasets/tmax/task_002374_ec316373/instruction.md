You are a data researcher organizing a large stream of dataset submissions. Unfortunately, some automated submissions are "poisoned" with artificially injected multi-collinearity, making them statistically unreliable for downstream modeling. You need to build a robust pipeline that detects and rejects these corrupted datasets.

Your task has two parts: System Setup and Data Science Detection.

### Part 1: System Setup (Pipeline Reproducibility)
You have a multi-service ingestion pipeline located in `/home/user/pipeline/`. The pipeline consists of:
1. **Redis Queue**: Runs on default port 6379.
2. **Flask Ingest API**: Runs on port 5000. It receives dataset paths and pushes them to Redis.
3. **Python Worker**: Reads from Redis, invokes a validation script (`/home/user/detector.py`), and moves the CSV file to `/home/user/accepted/` or `/home/user/rejected/` based on the script's exit code (0 for clean, 1 for evil).

Currently, the pipeline is misconfigured. 
- You must configure the worker (`/home/user/pipeline/worker.py`) by setting the correct environment variable `REDIS_URL=redis://localhost:6379/0` in its startup script `/home/user/pipeline/start_worker.sh`.
- Start the Redis server, Flask API (`/home/user/pipeline/api.py`), and the worker. 
- Ensure that if you `POST` a JSON payload `{"file_path": "/path/to/data.csv"}` to `http://localhost:5000/process`, the file is correctly routed by the worker.

### Part 2: Data Science Detection (Adversarial Corpus)
You need to write the validation script at `/home/user/detector.py`.

You are provided with labeled training datasets in:
- `/home/user/train_data/clean/`
- `/home/user/train_data/evil/`

The "evil" datasets look similar to clean ones but contain hidden linear dependencies (multi-collinearity). 
1. Perform correlation and covariance analysis on the training data.
2. Calculate the condition number of the covariance matrix for each dataset using linear algebra principles.
3. Use cross-validation to tune and find an optimal condition number threshold that perfectly separates the clean datasets from the evil ones.
4. Implement `/home/user/detector.py`. It must accept a single command-line argument (the path to a CSV file). It should compute the condition number, apply your discovered threshold, and **exit with code 0 if the dataset is clean, and exit with code 1 if the dataset is evil**.

You may use Python (e.g., `numpy`, `pandas`, `scikit-learn`) or R to write your scripts, but the entry point must be executable as `python3 /home/user/detector.py <path_to_csv>` (or via a bash wrapper).

Ensure your pipeline is running in the background and `/home/user/detector.py` is fully implemented.
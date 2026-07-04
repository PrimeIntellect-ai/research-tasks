You are an AI assistant helping a data scientist set up an automated data cleaning pipeline for sensor telemetry.

We have a multi-service architecture for processing CSV files, but it's currently broken and missing the core filtering logic.

The architecture consists of:
1. A Redis instance (supposed to run on default port 6379).
2. A Python Flask API (`/app/api.py`) running on port 5000. It provides an endpoint `POST /ingest` which accepts JSON `{"filepath": "/path/to/file.csv"}` and pushes the path to a Redis list named `processing_queue`.
3. A Go worker service that you need to write from scratch at `/home/user/worker/main.go`.

Your objectives:
1. **Model Discovery**: We have provided a labeled dataset at `/app/labeled_sensor_data.csv`. It contains continuous features `v1`, `v2`, `v3` and a `label` column (0 = clean, 1 = corrupted/evil). The corrupted rows can be separated by a simple linear combination of the features. Analyze this dataset to find the exact classification rule (thresholding a linear combination).
2. **Service Configuration**: Start Redis and the Flask API. You may need to inspect and modify `/app/api.py` as it currently has a misconfiguration preventing it from connecting to Redis properly.
3. **Go Worker Implementation**: Write a Go worker that:
   - Connects to Redis locally.
   - Continuously pops file paths from the `processing_queue` list (blocking pop).
   - Reads the CSV file at the given path.
   - Applies your discovered linear classification rule.
   - Writes *only* the clean rows (along with the CSV header) to `/home/user/output/<basename_of_file>`. For example, if the input is `/tmp/data1.csv`, output should be `/home/user/output/data1.csv`.
   - The worker must be compiled to `/home/user/worker_bin` and running in the background.

**Adversarial Corpus Verification:**
Once your pipeline is running, an automated verifier will test your system by sending POST requests to `http://127.0.0.1:5000/ingest`. 
It will feed files from two hidden corpora:
- Clean corpus: Contains files where 100% of the rows are valid. Your pipeline must preserve all data rows in the output.
- Evil corpus: Contains files where 100% of the rows are corrupted. Your pipeline must output files containing ONLY the CSV header.

**Requirements**:
- Ensure the output directory `/home/user/output/` exists.
- The Flask API must be accessible on port 5000.
- The Go worker must correctly parse the CSV, perform the linear algebra/thresholding efficiently, and write the output.
- Leave the services (Redis, Flask, Go worker) running in the background when you are done.
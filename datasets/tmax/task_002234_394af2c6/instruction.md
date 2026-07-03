You are an ML engineer preparing training data for a spectroscopy model. We have a localized multi-service pipeline that streams simulated spectral observations, buffers them, and runs a matrix factorization feature extraction on them. However, the pipeline is currently broken and crashing.

Your objective is to fix the pipeline, identify why the factorization is failing, and create a robust filter to sanitize the data stream.

Here is the current state of the system:
- The pipeline is located in `/app/services/` and contains three components: a Redis instance, a Data Emitter (Flask), and a Worker.
- You can start the system using the provided script `/app/services/start.sh`.
- The Data Emitter generates spectral matrices but is currently failing to connect to Redis due to a misconfiguration.
- Once connected, the Worker process pulls these matrices from Redis and applies Non-negative Matrix Factorization (NMF). However, the simulated data occasionally includes near-singular or rank-deficient matrices (e.g., from sensor anomalies or flat signals), which causes the factorization step to fail and the Worker to crash.

Your tasks:
1. **Fix the Pipeline Configuration**: Inspect the configuration files in `/app/services/emitter/` and correct the Redis connection settings so the Emitter can successfully push data to the queue. The Redis server runs locally on its default port.
2. **Develop a Data Sanitizer**: You must build an adversarial filter to detect these bad matrices. We have provided a corpus of training examples in `/app/corpus/clean/` (valid, well-conditioned spectral matrices) and `/app/corpus/evil/` (near-singular or rank-deficient matrices that crash the worker).
   - Create a Python script at `/home/user/filter_corpus.py`.
   - This script MUST contain a function with the exact signature: `def check_matrix(file_path: str) -> bool:`
   - The function should load the CSV file, analyze the matrix (e.g., using condition numbers, rank, or singular values), and return `True` if the matrix is "clean" and `False` if it is "evil".
3. **Integrate the Filter**: Modify the worker script at `/app/services/worker/worker.py` to import and use your `check_matrix` function. It should drop any incoming matrix that evaluates to `False` and only process `True` matrices.
4. **Verify Flow**: Ensure the `start.sh` script can run indefinitely without the Worker crashing, and that successful extractions are being logged to `/app/services/worker/success.log`.

Requirements:
- Your `check_matrix` function must achieve a 100% acceptance rate on the clean corpus and a 100% rejection rate on the evil corpus. 
- Do not hardcode filenames in your `check_matrix` function; it will be evaluated against a hidden holdout set with identical statistical properties.
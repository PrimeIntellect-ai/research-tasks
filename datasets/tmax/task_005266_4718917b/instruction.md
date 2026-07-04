You are assisting a data researcher who is organizing a massive repository of experimental datasets. Unfortunately, many datasets in the repository have been corrupted by a faulty data generation script, creating synthetic anomalies. You need to build and deploy a data filtering pipeline to reject these "evil" datasets while preserving the "clean" ones.

The system is composed of three services that must work together:
1. **Redis Server**: Acts as the message queue.
2. **Flask API**: An ingestion service located at `/app/api/app.py`. It provides an endpoint (`POST /validate`) that receives a dataset path, queues a job in Redis, and waits for the result. 
3. **C++ Detector Worker**: A background worker that pulls jobs from Redis, analyzes the dataset using a custom C++ program you must write, and returns the result.

### Your Objectives:

**1. Implement the C++ Anomaly Detector**
Create a C++ program at `/app/worker/detector.cpp` and compile it to `/app/worker/detector`. 
It must take a single command-line argument (the path to a CSV file) and output exactly one word to standard output: `VALID` or `ANOMALOUS`.

The CSV files have a header `id,signal,background,noise` followed by floating-point tabular data.
Your detector must flag the file as `ANOMALOUS` if it violates *either* of the following data science rules:
*   **Similarity Rule**: If any two distinct rows in the dataset have a cosine similarity $\ge 0.999$ (calculated using the `signal`, `background`, and `noise` columns as a 3D vector), the file is a synthetic duplicate.
*   **Hypothesis Testing Rule**: The `signal` column should theoretically have a population mean of $50.0$. Calculate the sample mean and the standard error of the mean ($SEM = \frac{s}{\sqrt{n}}$, where $s$ is the sample standard deviation). Calculate the 99.9% confidence interval for the mean using a Z-score of $3.29$. If the theoretical mean ($50.0$) falls strictly outside this calculated confidence interval, the file has drifted and is anomalous.

If neither rule is violated, output `VALID`.

**2. System Composition & Configuration**
*   Start the Redis server on its default port (`6379`).
*   The Flask API (`/app/api/app.py`) is missing its Redis connection configuration. Fix the environment variables or configuration so it connects to local Redis. Run the API on port `5000`.
*   A worker script (`/app/worker/worker.sh`) is provided. It listens to Redis and calls your `./detector` binary. Start this worker.

**3. Adversarial Corpus Verification**
Your detector will be tested against two sets of data:
*   `/app/corpora/clean/` : Contains valid experimental data. Your pipeline must accept 100% of these.
*   `/app/corpora/evil/` : Contains data with synthetic duplications or statistical drift. Your pipeline must reject (flag as `ANOMALOUS`) 100% of these.

You can test your system end-to-end using the provided verification script: `/app/tests/run_tests.py`. Make sure all services are running and your C++ program is correctly compiled before running it. Leave all services running in the background when you are done.
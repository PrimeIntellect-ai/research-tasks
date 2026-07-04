You are an ML Engineer preparing a data preprocessing pipeline in Rust. We have a multi-service setup consisting of a Redis database for experiment tracking and a Rust web service for dataset preparation. 

Currently, the Rust service has a critical data leakage bug in its numerical scaling logic, and it is missing the experiment tracking integration.

Your task is to fix the bug, implement the tracking, and bring up the services.

The system is located in `/app/data_service`. 
In this directory, you will find a skeleton Rust Actix-web server (in `src/main.rs`) and a `Cargo.toml`. 

Here is what you need to do:

1. **Fix the Data Leak:**
   The service exposes an HTTP POST endpoint at `/prepare`. It accepts a JSON array of `f64` arrays representing numerical token features (e.g., `[[1.0, 2.0], [3.0, 4.0]]`).
   The code currently generates 5 bootstrap samples (randomly sampled rows with replacement) from the input dataset. It then combines the original data and the bootstrap samples, calculates the column-wise mean and standard deviation of the *combined* dataset, and standardizes (z-score normalizes) everything. 
   This is a classic data leak! The scaling parameters (mean and std dev) must be computed **ONLY** on the original input dataset, and then applied to both the original dataset and the generated bootstrap samples. Update the Rust code to fix this. Use a standard deviation of 0.0 if the calculated standard deviation is 0 (to avoid division by zero).

2. **Implement Experiment Tracking:**
   After scaling, the service must connect to a local Redis instance (on `127.0.0.1:6379`) and log a metric. Calculate the absolute maximum value across all scaled elements in the *original* dataset. Set this value in Redis as a string under the key `experiment:latest:max_abs_val`. Use the `redis` crate.

3. **Service Orchestration:**
   - Start a local `redis-server` running in the background on port 6379.
   - Build and run the Rust web service so that it listens on `127.0.0.1:3000`.
   - The `/prepare` endpoint must return the scaled original dataset and scaled bootstrap samples as a JSON response in this exact format:
     `{"original": [[...], ...], "bootstraps": [[[...], ...], ...]}`

Ensure both the Redis server and the Rust HTTP service are running at the end of your process. You do not need to set up Nginx, but ensure the Rust service strictly listens on `127.0.0.1:3000`.
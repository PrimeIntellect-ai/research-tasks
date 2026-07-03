You are an MLOps engineer debugging an experiment tracking pipeline that suffers from data leakage and configuration errors. 

The system consists of three services running locally:
1. A Redis instance acting as an artifact queue.
2. A Flask API (`/app/experiment_api.py`) that receives raw experiment data batches.
3. A background worker (`/app/worker.py`) that reads batches from Redis, preprocesses them, computes correlation metrics, and posts the results back to the Flask API.

Currently, the pipeline is broken in two ways:
First, the services are misconfigured. The startup script `/app/start_services.sh` brings up Redis, the API, and the worker, but the worker fails to communicate with the API and Redis due to mismatched ports and environment variables. You must modify `/app/worker.py` and `/app/experiment_api.py` (or their configurations) so that the end-to-end flow works: The API runs on port 5000, Redis on 6379, and the worker successfully pops items from the `experiment_queue` and POSTs back to `http://localhost:5000/log_metric`.

Second, the current preprocessing logic leaks data (a classic `fit_transform` leakage over the entire dataset instead of using causal/historical statistics) and crashes on schema violations. You must replace the preprocessing script by writing a new standalone Python executable at `/home/user/preprocessor.py`. 

The `preprocessor.py` script must strictly obey the following behavior to pass rigorous equivalence testing:
- **Input:** Reads a JSON array of dictionaries from `stdin`. Each dictionary represents a time-step with keys `"f1"` and `"f2"` (values are floats or `null`).
- **Schema Enforcement:** Any dictionary that does not contain BOTH keys `"f1"` and `"f2"` (even if `null`) must be completely removed from the sequence before further processing.
- **Outlier Handling:** Any non-null float value strictly less than `-5.0` must be clipped to `-5.0`. Any non-null float strictly greater than `5.0` must be clipped to `5.0`.
- **Missing Value Handling (Strictly Causal):** If a value for `"f1"` or `"f2"` is `null`, it must be imputed using the mean of all *preceding* valid (and clipped) values for that specific feature in the sequence. If the very first value(s) in the sequence is `null`, impute it with `0.0`.
- **Correlation Analysis:** After imputation, compute the Pearson correlation coefficient between the cleaned `"f1"` and `"f2"` arrays. If the variance of either feature is zero or there are fewer than 2 data points, output `0.0`. Round the correlation to exactly 4 decimal places.
- **Output:** Print a JSON object to `stdout` strictly in this format:
  `{"cleaned_data": [{"f1": float, "f2": float}, ...], "correlation": float}`

Write `/home/user/preprocessor.py` and ensure it is executable (`chmod +x`). Then ensure the multi-service pipeline correctly routes data. The verifier will fuzz your `preprocessor.py` against a hidden oracle with thousands of random JSON sequences to ensure bit-exact output equivalence, and it will trigger an API request to verify the pipeline integration.
You are a machine learning engineer tasked with preparing training data and building a small data-serving API. You must fix a broken vendored library, process a dataset with strict reproducibility guarantees, compute statistical metrics, and serve the results over an HTTP API.

Step 1: Fix the Vendored Package
We rely on a proprietary data preparation library shipped at `/app/vendor/ml_prep_lib-0.1.0`. 
Currently, it has two problems:
1. It cannot be installed because its `Makefile` contains a typo in the installation command.
2. Inside `ml_prep_lib/core.py`, the `merge_sensor_data(df_main, df_ref)` function performs a pandas merge that introduces NaNs. This silently converts the `sensor_hash` column (which contains 64-bit integers larger than $2^{53}$) into `float64`, causing catastrophic precision loss for our downstream cryptographic validations. 
Fix the `Makefile` and modify `core.py` to use pandas' nullable integer data type (`"Int64"`) for the `sensor_hash` column before or during the merge so that precision is perfectly preserved. Install the fixed package in your environment.

Step 2: Data Processing and Experiment Tracking
We have two datasets: `/home/user/main_sensors.csv` and `/home/user/ref_sensors.csv`.
Write a script `/home/user/pipeline.py` that:
1. Loads both CSVs.
2. Uses `ml_prep_lib.core.merge_sensor_data` to merge them.
3. Performs a 2-sample Welch's t-test (unequal variances) comparing the numerical `signal_strength` between rows where `environment == 'urban'` and rows where `environment == 'rural'`. Calculate the p-value and the 95% confidence interval for the difference in means (urban - rural).
4. Extracts the columns `feature_1` through `feature_5`, centers them (subtract the mean), and computes the first principal component (a vector of length 5) using Linear Algebra (e.g., SVD or PCA). 
5. Saves an experiment tracking file at `/home/user/exp_results.json` containing the test statistics and the PCA vector.

Step 3: Serve the Results via API
Create and start a web service (e.g., using FastAPI or Flask) listening exactly on `127.0.0.1:8080`.
The service must enforce authentication: requests must include the header `Authorization: Bearer ds-auth-token-999`. Return a 401 Unauthorized if missing or incorrect.

The service must expose the following HTTP GET endpoints:
- `GET /pca`: Returns a JSON response `{"top_component": [v1, v2, v3, v4, v5]}` where the values are the elements of the first principal component, rounded to 4 decimal places.
- `GET /test`: Returns a JSON response `{"p_value": p, "ci_lower": lower, "ci_upper": upper}` representing the Welch's t-test results, rounded to 4 decimal places.

Leave the API running in the background so it can be verified. Ensure all scripts and services are fully reproducible.
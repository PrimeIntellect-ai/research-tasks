You are a Data Engineer tasked with fixing and running an ETL pipeline. 

The pipeline ingests data from two sources, performs data fusion, applies a linear algebraic transformation, runs a Bayesian inference step, and tracks the results. However, the current implementation is incomplete and buggy.

**Environment Setup & Data Sources:**
1. A background local API server will be running on `http://127.0.0.1:8080/data`. It serves JSON data containing: `id`, `reading_2`, `trials`, and `successes`.
2. A local CSV file exists at `/home/user/data/sensors.csv` containing: `sensor_id` and `reading_1`.

**Your Tasks:**

1. **Schema Enforcement & Multi-source Joining:**
   - Read `/home/user/data/sensors.csv`. Notice that the `sensor_id` column contains missing values (NaNs), which silently converts the column from integer to float in pandas.
   - You must enforce a strict integer schema for the `sensor_id`. Drop any rows where `sensor_id` is missing, and explicitly cast the column to the pandas nullable integer type (`Int64`) or standard `int` BEFORE joining.
   - Fetch the JSON data from `http://127.0.0.1:8080/data`.
   - Perform an inner join between the CSV data and the API data on `sensor_id` == `id`.

2. **Linear Algebra Feature Transformation:**
   - Create a feature matrix $X$ of shape $(N, 2)$ from the columns `[reading_1, reading_2]` of the joined data.
   - We have a projection matrix $P = \begin{bmatrix} 0.5 & 0.2 \\ 0.1 & 0.8 \end{bmatrix}$.
   - Apply the transformation $X' = X P$.
   - Extract the first column of the transformed matrix $X'$ as a new feature `projected_f1`.

3. **Bayesian Inference:**
   - The API provides the number of Bernoulli `trials` and `successes` for each sensor.
   - Assume a Beta prior distribution for the success probability with $\alpha = 2$ and $\beta = 2$.
   - Calculate the posterior mean for each sensor using the conjugate prior update rule: 
     $\text{Posterior Mean} = \frac{\alpha + \text{successes}}{\alpha + \beta + \text{trials}}$

4. **Experiment Tracking:**
   - Calculate two final aggregate metrics:
     1. `sum_projected_f1`: The sum of the `projected_f1` feature across all joined rows.
     2. `average_posterior_mean`: The average of the calculated posterior means across all joined rows.
   - Save these metrics to an experiment tracking file at `/home/user/experiment_results.json`. The file must be valid JSON with exactly these two keys.

Write a Python script at `/home/user/run_etl.py` that implements all the above logic.
Before running your script, ensure you have started the API server (you will need to write a simple mock server at `/home/user/api_server.py` that listens on port 8080 and serves the data, or assume one is provided if I gave it to you. Wait, I will provide the API server and data for you. Just start it).

Actually, the setup is as follows:
- The CSV is at `/home/user/data/sensors.csv`.
- The API server script is at `/home/user/api/server.py`. You must start it in the background (e.g., `python /home/user/api/server.py &`) and wait a second for it to initialize before running your ETL script.

Execute your ETL script and ensure `/home/user/experiment_results.json` is generated correctly.
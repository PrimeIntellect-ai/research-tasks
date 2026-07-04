You are acting as a Data Analyst for a sensor network company. You have a set of raw CSV files containing sensor readings. You need to build an ETL script to process these files, perform statistical analysis, and then serve the results using a provided internal web server package.

Step 1: Data Processing & ETL
- You will find raw sensor data in `/home/user/data/raw/`. There are multiple CSV files. Each file has the columns: `timestamp`, `sensor_id`, `group`, and `value`. The `group` column contains either "A" or "B".
- Read and combine all CSV files.
- **Missing Values**: Drop any rows where the `value` column is missing (NaN/null).
- **Outlier Handling**: For each group independently, calculate the Interquartile Range (IQR = Q3 - Q1). Remove any rows where the `value` is strictly less than Q1 - 1.5*IQR or strictly greater than Q3 + 1.5*IQR.
- **Statistical Analysis**: On the cleaned dataset:
  1. Calculate the mean `value` for Group A and Group B.
  2. Calculate the 95% Confidence Interval for the mean of each group (assuming a normal distribution for the sample mean, you can use the t-distribution or z-distribution standard approximations).
  3. Perform a Welch's t-test (two-tailed, unequal variances) to compare the means of Group A and Group B.
- Save the results as a JSON file at `/home/user/data/processed/results.json` with the following exact keys:
  `group_a_mean`, `group_a_ci_lower`, `group_a_ci_upper`, `group_b_mean`, `group_b_ci_lower`, `group_b_ci_upper`, `t_statistic`, `p_value`.

Step 2: Fix and Deploy the Vendored Server
We have a pre-packaged internal API server located at `/app/statsserver/`. 
- The server is a Python Flask application that serves the JSON results file over HTTP.
- There is a deliberate bug in the `Makefile` located in `/app/statsserver/`. The server expects an environment variable `STATS_DATA_PATH` pointing to the JSON file you created, but the Makefile exports the wrong variable name and attempts to bind to the wrong port (it must listen on `127.0.0.1:8080`).
- Fix the `Makefile` so that `make serve` correctly sets the environment variable to `/home/user/data/processed/results.json` and runs the server on `127.0.0.1:8080`.
- Start the server in the background using `make serve`.

Verification Requirements:
The automated verifier will make an HTTP GET request to `http://127.0.0.1:8080/api/stats`.
You must ensure the server correctly authenticates the request using the exact token: `Bearer token-stats-2024`. The server code already implements this auth check, you just need to ensure the server is running and returning your processed data.

Do not use root privileges. You can write your ETL scripts in any language you prefer.
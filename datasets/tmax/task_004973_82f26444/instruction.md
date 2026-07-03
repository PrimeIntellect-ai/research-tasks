We have a local data ingestion pipeline that receives sensor measurements via an API. The pipeline consists of three services: Nginx, a Flask API, and Redis. However, the system is currently broken, and we need a data analyst/engineer to fix the configuration and build a robust data validation script.

First, fix the multi-service setup:
1. The Nginx configuration file is located at `/app/nginx.conf`. It is currently misconfigured to forward traffic on port 8080 to port 8000. Modify it so that it correctly proxies requests to the Flask app, which runs on port 5000.
2. Once fixed, start the services by running the provided script: `bash /app/start.sh`.

Second, we need to filter out anomalous or maliciously crafted data payloads. Create a Python script at `/home/user/validate_data.py`. This script will be executed with a single argument: the absolute path to an incoming CSV data file.

The input CSV contains three columns: `sensor_id`, `timestamp`, and `value`.
There is also a static metadata file located at `/app/sensor_metadata.csv` containing two columns: `sensor_id` and `status`.

Your script must implement the following exact logic to classify the data:
1. **Multi-source Join**: Read the input CSV and inner-join it with `/app/sensor_metadata.csv` on `sensor_id`. Only retain rows where the sensor `status` is `'active'`.
2. **Missing Value Handling**: Check the `value` column of the joined, active data. If strictly more than 10% of these rows have missing values (NaN or empty) in the `value` column, reject the file. Otherwise, drop the rows with missing `value`s.
3. **Outlier Removal**: Remove any rows where the `value` is an outlier. An outlier is defined as a value that is strictly more than 3 sample standard deviations away from the sample mean of the `value` column.
4. **Hypothesis Testing**: Using the cleaned data (after joining, dropping NaNs, and removing outliers), conduct a 1-sample t-test to check if the true mean of the `value` column is exactly `50.0`. Reject the file if the two-sided p-value is strictly less than `0.01` (indicating statistical significance that the mean is not 50.0).

Output format for `/home/user/validate_data.py`:
- If the file passes all criteria, the script must print exactly `ACCEPT` to standard output and exit with status code `0`.
- If the file fails ANY of the criteria, the script must print exactly `REJECT` to standard output and exit with status code `1`.
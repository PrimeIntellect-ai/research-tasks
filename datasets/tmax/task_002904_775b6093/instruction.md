As a data analyst, you have been tasked with cleaning up a messy time-series dataset from our IoT temperature sensors. A flaky ETL job has been retrying upon failure, resulting in duplicate and jittery records. Furthermore, network drops have caused gaps in our time series.

You need to write a script (Bash, awk, or Python) to process the raw CSV file located at `/home/user/raw_sensors.csv` and generate a cleaned, normalized dataset at `/home/user/processed_sensors.csv`.

Here are the specific requirements for the data pipeline:
1. **Time-based Bucketing**: Group the data into 5-minute (300-second) buckets. The bucket timestamp should be calculated as `floor(timestamp / 300) * 300`.
2. **Deduplication / Aggregation**: Because of the ETL retries and jitter, multiple temperature readings may fall into the same 5-minute bucket for a given sensor. Resolve this by taking the MAXIMUM temperature recorded in that bucket.
3. **Imputation (Forward Fill)**: For each sensor, there must be a contiguous set of 5-minute buckets from its earliest recorded bucket to its latest recorded bucket. If any 5-minute buckets are missing in between, fill them by carrying forward the maximum temperature from the immediately preceding bucket.
4. **Output Format**: The output file `/home/user/processed_sensors.csv` must include a header `bucket_timestamp,sensor_id,temperature`. The rows must be sorted ascending first by `sensor_id`, and then ascending by `bucket_timestamp`.

Ensure your output matches these rules precisely. Keep temperatures formatted to one decimal place (e.g., `21.0`).
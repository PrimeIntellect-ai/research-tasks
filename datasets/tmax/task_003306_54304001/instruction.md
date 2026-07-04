You are a data engineer tasked with building a streaming ETL pipeline in Rust. 

We have a multi-service architecture simulating a real-time data stream:
1. **Source Service**: A data generator writing raw JSON records to a named pipe at `/tmp/raw_data.pipe`.
2. **Sink Service**: A data accumulator reading processed JSON records from a named pipe at `/tmp/processed_data.pipe`.

Your objective is to build a Rust application that bridges these two services. It must read line-by-line from the source pipe, apply specific data transformations and aggregations to handle missing values and outliers, and write the cleaned data line-by-line to the sink pipe.

**Data Format**:
Input records look like this: `{"timestamp": 1700000000, "sensor_id": "A", "value": 45.2}`. Sometimes the `"value"` key is missing or set to `null`. Sometimes it contains extreme outliers.

**Transformation Requirements**:
To prevent "data leakage" (using future data to normalize past data), you must process records strictly sequentially:
1. **Missing Value Imputation (Forward Fill)**: Group data by `sensor_id`. If a value is missing or null, replace it with the most recent valid (or imputed/clipped) value for that sensor. If it's the very first record for a sensor and it's missing, use `0.0`.
2. **Outlier Clipping**: Maintain a rolling window of the last `20` final (post-imputed/clipped) values for each `sensor_id`. 
   - Calculate the mean and standard deviation of this window *before* adding the current value. (If the window has fewer than 2 elements, standard deviation is 0.0, and no clipping occurs).
   - Calculate the Z-score of the current value. If the Z-score is greater than `3.0` or less than `-3.0`, clip the value to exactly `mean + 3 * stddev` or `mean - 3 * stddev`, respectively.
   - *Crucial*: Update the rolling window with the *final* (possibly clipped) value only *after* evaluating it. 
3. **Format**: Output the transformed records to `/tmp/processed_data.pipe` as single-line JSON objects with the exact same keys: `{"timestamp": ..., "sensor_id": ..., "value": ...}` (where `value` is the final cleaned float).

**System Setup**:
- Create a new Rust project at `/home/user/etl_worker`. You may use `serde`, `serde_json`, and `anyhow`.
- The source and sink services are started by running `/app/start_services.sh`. Ensure your Rust app runs concurrently and successfully processes the stream until the source pipe closes.

Write, compile, and run your Rust application so that the sink service receives the data. The automated test will evaluate your solution based on the Mean Squared Error (MSE) of your output values compared to the mathematical ground truth.
You are a data engineer for an IoT analytics company. We need to build a highly performant ETL and modeling pipeline in Rust.

Your task is to create a Rust project in `/home/user/iot_pipeline` that reads raw sensor data, performs feature engineering, fits a mathematical Ordinary Least Squares (OLS) regression model, benchmarks the inference speed, and outputs the results.

Here are the specific requirements:

1. **Input Data**: The raw data is located at `/home/user/data/raw_sensors.csv`. It has a header and four columns: `id`, `sensor_1`, `sensor_2`, and `target`. All data is given as floating-point numbers (except `id`, which is an integer).

2. **ETL Process**:
   - Read the CSV file.
   - Filter out (drop) any rows where `sensor_1 < 0.0` or `sensor_2 < 0.0`.
   - Create a new engineered feature: `sensor_3 = sensor_1 * sensor_2`.
   - Your design matrix $X$ for the OLS model should consist of a column of 1s (for the intercept), followed by `sensor_1`, `sensor_2`, and `sensor_3`.
   - Your target vector $y$ is the `target` column.

3. **Mathematical Modeling**:
   - Using the `nalgebra` crate, calculate the exact OLS regression weights using the formula: $\beta = (X^T X)^{-1} X^T y$.
   - The resulting vector $\beta$ will contain the intercept as its first element, followed by the weights for `sensor_1`, `sensor_2`, and `sensor_3`.

4. **Inference Benchmarking**:
   - Write a function to perform inference (matrix multiplication of $X$ and $\beta$) on the entire cleaned dataset.
   - Run this inference function in a loop 1,000 times. Measure the total time taken for the 1,000 iterations and calculate the average time per single dataset inference in microseconds.

5. **Output**:
   - Save the model metrics to a JSON file at `/home/user/model_metrics.json` with the following exact structure:
   ```json
   {
     "intercept": 1.2345,
     "weights": [0.123, 0.456, 0.789],
     "avg_inference_micros": 45.2
   }
   ```
   *(Note: The numbers above are examples. Your JSON must contain your calculated `intercept` (float), the 3 feature `weights` (array of floats), and the `avg_inference_micros` (float).)*

Ensure your Rust project compiles correctly using `cargo build --release` and runs without errors. You may use standard crates such as `csv`, `serde`, `serde_json`, and `nalgebra`.
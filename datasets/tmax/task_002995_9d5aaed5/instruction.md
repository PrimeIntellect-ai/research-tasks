You are a data analyst tasked with processing an industrial IoT sensor dataset using Rust. 
The dataset is located at `/home/user/sensor_data.csv` and contains three columns: `timestamp` (integer), `sensor_id` (string), and `value` (float).

Your goal is to write a Rust program that acts as a data pipeline. You must create a new Rust project in `/home/user/sensor_processor`. Your program must read `/home/user/sensor_data.csv`, process the data according to the rules below, and write the anomalous records to `/home/user/anomalies.csv`.

Processing Rules:
1. **Constraint-based validation**: Filter out and completely ignore any rows where the `value` is less than `-50.0` or greater than `150.0`. Also ignore rows that have malformed data.
2. **Stratified Sampling**: We only want to process a sample of the valid data. For each unique `sensor_id`, keep only every 5th valid row. Use a 0-based counter for each sensor. (i.e., keep the 1st valid row (index 0), 6th valid row (index 5), 11th valid row (index 10), etc., for each sensor independently).
3. **Anomaly Detection**: For the rows that are kept after step 1 and step 2, track the temperature changes. If the absolute difference between a sensor's current kept `value` and its *previously kept* `value` is strictly greater than `20.0`, flag this current row as an anomaly. The very first kept row for any sensor cannot be an anomaly (as there is no previous value to compare to).

Output:
Your Rust program should produce `/home/user/anomalies.csv` with the headers: `timestamp,sensor_id,value,delta`. 
`delta` is the absolute difference that triggered the anomaly, formatted to exactly one decimal place (e.g., `25.0`).
Write all anomalous records to this file in the exact order they were detected from the top-to-bottom reading of the source file.

Once your code is written, compile and run it to produce the `anomalies.csv` file. Do not use any external crates other than standard library, or optionally `csv` and `serde` if you wish, but standard library string manipulation is sufficient.
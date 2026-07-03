As a machine learning engineer, you are preparing observational sensor data to be used as training inputs for a predictive model. Before feeding the raw time-series data into the neural network, you need to establish a baseline linear trend for a specific sensor to normalize the inputs.

You have a raw dataset located at `/home/user/raw_sensor_data.csv` with the following CSV format:
`timestamp_ms,sensor_id,temperature`

Your task is to orchestrate a small pipeline that reshapes this data and fits a linear regression model using Rust and standard bash utilities.

Perform the following steps:
1. Reshape the data: Extract only the records for `sensor_id` equal to `SENS-42`.
2. Normalize the time: Convert the `timestamp_ms` to relative time in seconds ($t_{relative}$), where the very first reading for `SENS-42` represents $t=0$. (e.g., a timestamp 1000ms after the first reading is $t=1.0$). 
3. Curve Fitting: Write a standalone Rust program at `/home/user/trend_fitter.rs` (which you should compile with `rustc`) that takes the reshaped data and calculates a simple linear regression (least squares fit) to find the slope ($m$) and intercept ($c$) for the equation: `temperature = m * t_relative + c`.
4. Orchestrate: Run your pipeline and save the final regression results to a log file at `/home/user/regression_results.txt`.

The final output file `/home/user/regression_results.txt` must contain exactly one line in this precise format (rounded to 4 decimal places):
`Slope: <m>, Intercept: <c>`

Example of expected output format:
`Slope: 0.1234, Intercept: 12.3456`

Constraints:
- You must use standard bash tools (like `awk`, `grep`, `sed`, etc.) for the data reshaping steps or orchestrate them within the Rust program.
- Do not use external Rust crates (no `Cargo.toml` needed); rely only on the Rust standard library for parsing and calculating the linear regression.
- Assume `rustc` is available in the environment.
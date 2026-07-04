You are a performance engineer profiling a new server application. You have collected raw telemetry data from a hardware sensor, but the logging framework mixed the numerical data with unstructured text. You need to orchestrate a pipeline to reshape this observational data and perform a statistical signal analysis using numerical integration and differentiation.

The raw telemetry data is located at `/home/user/raw_telemetry.log`.
The file contains lines like this:
`[LOG] t=0.0s | sensor_pwr=10.0W | status=idle`

Your task is to:
1. Reshape the Data: Write a bash script (or command) to parse `/home/user/raw_telemetry.log` and extract only the time (`t`) and power (`sensor_pwr`) values as a comma-separated format without units (e.g., `0.0,10.0`). Save this cleaned data to `/home/user/clean.csv`.
2. Analyze the Signal: Write a Rust program at `/home/user/analyze.rs` that reads `/home/user/clean.csv`. The Rust program must:
   - Calculate the numerical derivative of the power with respect to time (forward difference method: `(pwr_next - pwr_current) / (t_next - t_current)`) for each consecutive pair of points. Find the maximum derivative value.
   - Calculate the total energy consumed over the entire period by numerically integrating the power over time using the Trapezoidal rule.
3. Generate Report: The Rust program should output the final results to a file named `/home/user/report.txt` in the exact following format (rounded to 2 decimal places):
   ```
   Max Power Derivative: <value>
   Total Energy: <value>
   ```

You must ensure that your Rust code compiles cleanly and writes exactly the required output format.
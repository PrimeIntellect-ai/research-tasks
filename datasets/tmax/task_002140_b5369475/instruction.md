You are a data scientist tasked with cleaning a messy dataset of sensor logs and performing basic statistical analysis. 

The raw data is located at `/home/user/sensor_logs.txt`. This file contains unstructured text from a faulty sensor logging system. Each line may contain a temperature reading in Celsius, but the format is inconsistent. Some lines contain corrupted data or no numerical data at all.

Your task is to write a Rust program to process this data and compute statistical metrics. 

Perform the following steps:
1. Initialize a new Rust project called `temp_analyzer` in `/home/user/temp_analyzer`.
2. Add any necessary dependencies (e.g., for statistical distributions or regex) to your `Cargo.toml`.
3. Write a Rust program that tokenizes each line in `/home/user/sensor_logs.txt` and extracts the valid temperature values. A valid temperature is any sequence of characters that can be successfully parsed as an `f64`. Skip any lines or tokens that do not contain a valid parseable float or represent corrupted text (e.g., "N/A", "err"). Note: Some lines might contain numbers that are part of text like "Sensor-1", ignore these if they don't parse cleanly as standalone floats when split by whitespace. Only extract the standalone floats representing the temperatures.
4. Calculate the following metrics on the extracted sample of valid temperatures:
   - Sample Mean
   - Sample Standard Deviation
   - The 95% Confidence Interval (Lower and Upper bounds) for the mean, using the Student's t-distribution appropriate for the sample size.
5. Your program must output these results to a JSON file at `/home/user/summary.json`. The JSON must have exactly the following keys: `"mean"`, `"std_dev"`, `"ci_lower"`, `"ci_upper"`.
6. Round all numerical values in the JSON output to exactly two decimal places.

Run your Rust program so that `/home/user/summary.json` is generated successfully.
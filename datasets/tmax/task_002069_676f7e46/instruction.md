You are a data analyst tasked with fixing and improving a broken data pipeline. 

We have IoT sensor data coming from multiple sites, stored as CSV files in `/home/user/input_data/`. 
A previous analyst tried to process these using standard command-line tools, but their pipeline silently dropped or corrupted rows because the `notes` column frequently contains embedded newlines (e.g., `"Routine check\nAll good"`).

You need to create a robust data processing script (using Python, R, or any suitable language of your choice) that handles these embedded newlines correctly and performs the following operations:

1. **Parallel Processing:** Process all CSV files in `/home/user/input_data/` concurrently. There are 4 files (`site_1.csv`, `site_2.csv`, `site_3.csv`, `site_4.csv`).
2. **Reshaping (Wide to Long):** The input files have the format: `timestamp,sensor_alpha,sensor_beta,sensor_gamma,notes`. You must reshape this so that the sensor columns are unpivoted into two columns: `sensor_name` (containing 'sensor_alpha', 'sensor_beta', or 'sensor_gamma') and `reading` (the numeric value).
3. **Cleaning:** Drop any rows where the `reading` is empty or NaN.
4. **Windowed Aggregation:** For each `site` (derived from the filename, e.g., `site_1`), and each `sensor_name`, sort the records chronologically by `timestamp`. Then, calculate a 3-period simple moving average (rolling average) of the `reading` column. Use a minimum period of 1 (i.e., the first row's average is just its own reading, the second is the average of the first two, etc.). Round the rolling average to 2 decimal places.
5. **Output:** Combine the results from all files and write them to a single CSV file at `/home/user/output_data/processed_combined.csv`. 

The final CSV must have exactly these headers:
`site_id,timestamp,sensor_name,reading,rolling_avg,notes`

Ensure the `notes` column retains its embedded newlines, enclosed in double quotes as per standard CSV formatting.

Your script must be entirely self-contained, handling dependency installations if you need specific libraries (like `pandas`), and you must execute it to generate the final output. The output directory `/home/user/output_data/` has already been created.
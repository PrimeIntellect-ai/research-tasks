You are tasked with building a robust data processing pipeline in Rust for a fleet of IoT sensors. You have two raw CSV files containing sensor metadata and time-series readings. Your goal is to create a Rust project that joins these sources, engineers new features, aggregates the data, and writes out a summary report.

**Input Data**:
1. `/home/user/data/sensors.csv`
Schema: `sensor_id` (integer), `location` (string), `sensor_type` (string)

2. `/home/user/data/readings.csv`
Schema: `timestamp` (string), `sensor_id` (integer), `value` (float)

**Task Requirements**:
1. Initialize a new Rust project named `sensor_pipeline` in `/home/user/sensor_pipeline`.
2. You may use any Rust crates you need (e.g., `polars`, `csv`, `serde`). Polars is highly recommended for tabular operations. Configure your `Cargo.toml` appropriately.
3. Write a Rust program (`src/main.rs`) that performs the following data processing steps:
   - **Join**: Merge the readings and sensors data on the `sensor_id` column.
   - **Filter**: Keep only the rows where `sensor_type` is exactly `"Temperature"`.
   - **Feature Engineering**: Create a new column called `temp_fahrenheit` by applying the formula: `(value * 1.8) + 32.0`.
   - **Aggregation**: Group the data by `location`. For each location, calculate:
     - The maximum `temp_fahrenheit` (name this column `max_temp_f`).
     - The average `temp_fahrenheit` (name this column `avg_temp_f`).
   - **Sorting**: Sort the resulting aggregated data alphabetically by `location`.
4. The program must write the final dataframe to a CSV file at `/home/user/output/aggregated_temps.csv`.
5. Run your Rust program so that the output file is generated.

**Output Format Constraint**:
The output CSV must have exactly these column headers in this order: `location,max_temp_f,avg_temp_f`. Ensure the float values are printed cleanly (e.g., `72.5`, `86.0`).

Ensure all output directories exist before writing.
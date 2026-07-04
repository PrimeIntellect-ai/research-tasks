Act as a Senior Machine Learning Engineer. We need to build a lightweight, reproducible data preparation pipeline exclusively using standard Linux command-line tools (Bash, awk, sed, etc.). Python, R, and other high-level languages are NOT allowed for this pipeline.

You need to write a standalone Bash script named `/home/user/pipeline.sh` that processes a raw sensor dataset, enforces schema validity, aggregates statistics, computes mathematical correlations, and logs the experiment metadata. 

Here are the requirements:

1. **Input Data**: The raw data will be at `/home/user/raw_sensors.csv`. It has a header and four columns: `sensor_id,temp_c,pressure_hpa,vibration_hz`.
2. **Schema Enforcement (Filtering)**: 
   The script must read the input file and output a cleaned file to `/home/user/cleaned_sensors.csv`.
   A row is only valid if it meets ALL the following schema constraints:
   - `sensor_id` is an integer (can be verified with regex or standard awk integer checks).
   - `temp_c` is between -50.0 and 150.0 inclusive.
   - `pressure_hpa` is between 800.0 and 1200.0 inclusive.
   - `vibration_hz` is between 0.0 and 5000.0 inclusive.
   - No fields are empty or non-numeric.
   The cleaned file must preserve the original header.
3. **Mathematical Analysis**: 
   Using the cleaned data (excluding the header), calculate the Pearson correlation coefficient ($r$) between `temp_c` (X) and `pressure_hpa` (Y). 
   Use `awk` to compute this mathematically in your bash script. Round the final correlation to 4 decimal places.
4. **Experiment Tracking**:
   The script must append a JSON-formatted single line to `/home/user/experiments.log` capturing the run's metadata. The JSON object must strictly match this structure (no spaces around keys, exact quoting):
   `{"timestamp":"<UNIX_EPOCH_SECONDS>","input_rows":<TOTAL_RAW_ROWS_EXCLUDING_HEADER>,"valid_rows":<CLEANED_ROWS_EXCLUDING_HEADER>,"temp_pressure_correlation":<CALCULATED_PEARSON_R>}`

Ensure your script is executable (`chmod +x /home/user/pipeline.sh`) and runs without user interaction.
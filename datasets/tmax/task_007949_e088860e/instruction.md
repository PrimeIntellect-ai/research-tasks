You are a data scientist working with a continuous stream of IoT environmental sensor data. The raw data often contains erroneous readings due to hardware glitches. Before feeding this data into downstream machine learning models, you need to write a robust C++ data pipeline to clean, validate, and normalize the data using a rolling statistical window.

Your task is to write a C++ program that reads a CSV file of raw sensor data, applies strict quality gates, computes rolling statistics on valid data, and normalizes the temperature readings.

**Data Inputs:**
You are provided with a raw dataset at: `/home/user/raw_sensor_data.csv`.
The CSV has a header and four columns: `timestamp,sensor_id,temperature,humidity`

**Requirements:**

1. **Write the C++ Application:**
   Create a C++ program at `/home/user/process_data.cpp`. It must use only the standard C++ library (no external dependencies like Boost or OpenCV). 

2. **Validation Checkpoints (Quality Gates):**
   Process the CSV row by row. Validate the `temperature` and `humidity` fields.
   - `temperature` must be between `-50.0` and `50.0` (inclusive).
   - `humidity` must be between `0.0` and `100.0` (inclusive).
   - If a row fails validation, do NOT include it in the rolling statistics. Instead, write it to `/home/user/rejected_data.csv`. 
   - The rejected CSV must have the header: `timestamp,sensor_id,temperature,humidity,error_reason`
   - The `error_reason` should be:
     - `invalid_temp` if only temperature is out of bounds.
     - `invalid_humidity` if only humidity is out of bounds.
     - `invalid_temp_and_humidity` if both are out of bounds.

3. **Rolling Statistics & Normalization:**
   For rows that PASS validation, maintain a **global rolling window of the last 5 valid temperature readings** (regardless of `sensor_id`).
   - When a new valid row is processed, add its temperature to the rolling window. If the window exceeds 5 items, discard the oldest.
   - Calculate the **Sample Mean** ($\mu$) and **Sample Standard Deviation** ($s$) of the current window.
   - Calculate the **Normalized Temperature** (Z-score) for the current row: $Z = (temperature - \mu) / s$.
   - **Edge cases:** If the window has fewer than 2 items, or if $s = 0.0$, output `0.0000` for both the standard deviation and the normalized temperature.

4. **Output Generation:**
   Valid rows must be written to `/home/user/cleaned_data.csv`.
   - The output CSV must have the header: `timestamp,sensor_id,temperature,humidity,rolling_mean,rolling_stddev,normalized_temp`
   - All newly calculated floating-point values (`rolling_mean`, `rolling_stddev`, `normalized_temp`) MUST be formatted to exactly **4 decimal places**. The original `temperature` and `humidity` can be printed as they were parsed, or to 1 decimal place.

5. **Compilation & Execution:**
   Compile your code using `g++ -O2 -std=c++17 /home/user/process_data.cpp -o /home/user/process_data` and run it to produce the output files.

Ensure your code handles the CSV header correctly and parses the fields accurately.
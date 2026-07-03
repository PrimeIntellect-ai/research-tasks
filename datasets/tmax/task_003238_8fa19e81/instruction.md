You are a data scientist tasked with cleaning a dataset of sensor readings and computing statistical anomalies. Standard bash tools are failing because the CSV contains embedded newlines within quoted fields, silently breaking naive pipeline tools. 

You must write a robust data processing pipeline in **C** to handle this data, calculate rolling statistics, and serve a generated report.

**Task Requirements:**

1. **The Data:**
   - A dataset is located at `/home/user/data/sensor_readings.csv`.
   - The CSV has headers: `timestamp,sensor_id,value,notes`.
   - The `notes` field is enclosed in double quotes (`"`) and frequently contains embedded newline characters (`\n`). Your C program must parse these correctly without breaking rows.

2. **The C Processing Program (`/home/user/pipeline/process.c`):**
   - Read the CSV data from standard input.
   - Filter rows to only process those where `sensor_id` is exactly `"S-100"`.
   - Extract the `value` column (which contains floating-point numbers).
   - Maintain a rolling window of the last `5` values for `S-100`.
   - Once the end of the file is reached, calculate the **population mean** and **population standard deviation** of this final window of 5 values.
   - Standardize these 5 values into Z-scores: `Z = (value - mean) / stddev`. (If stddev is 0, Z=0 for all).
   - Calculate the **Euclidean distance** between this 5-element Z-score vector and a reference vector: `[0.1, -0.2, 0.5, 1.0, -1.0]`. Note: the first element of your Z-score vector corresponds to the oldest value in the window of 5, and the 5th element is the newest value.
   - Use template-based text generation within your C code to print the output exactly in this JSON format to standard output:
     ```json
     {
       "sensor": "S-100",
       "latest_zscores": [Z1, Z2, Z3, Z4, Z5],
       "reference_distance": DISTANCE
     }
     ```
   - Float values should be printed with exactly 5 decimal places (e.g., `%.5f`).

3. **Orchestration & Serving:**
   - Compile your C program to `/home/user/pipeline/process`.
   - Run the data through your pipeline and save the output to `/home/user/public_html/report.json`.
   - Start a background web server using Python (`python3 -m http.server 8080`) rooted at `/home/user/public_html/`. Keep it running in the background.

Ensure your parsing logic correctly handles commas inside quotes if any, and strictly pairs double quotes to handle embedded newlines. Standard library usage only (no external C libraries like libcsv).
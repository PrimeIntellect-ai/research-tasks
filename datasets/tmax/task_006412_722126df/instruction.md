You are a data analyst working with a batch of sensor data files. You have been given a directory containing several CSV files, and you need to build a parallel data processing pipeline in Bash to calculate a specific mathematical metric for each file, logging the pipeline's progress, and outputting the final aggregated results in JSON format.

Here is the detailed specification for your task:

1. **Input Data**: 
   - Directory: `/home/user/data/`
   - Files: Multiple CSV files named `sensor_*.csv`.
   - Format: Each CSV has a header row `id,timestamp,reading`. The `reading` column contains integer values.

2. **Mathematical Operation**:
   - For each CSV file, calculate the **Sum of Squares** of the `reading` values, but **ONLY** for readings that are **odd numbers** (i.e., `reading % 2 != 0`).
   - If a file has no odd readings, the sum should be `0`.

3. **Processing & Parallelism Requirements**:
   - Write a Bash script at `/home/user/process.sh`.
   - Your script must process the CSV files in parallel (using background jobs `&`, `xargs -P`, or `parallel`).
   - Standard Unix tools (like `awk`, `sed`, `grep`, `jq`) should be used within your Bash script. 

4. **Logging**:
   - Your script must append to a log file at `/home/user/pipeline.log`.
   - Before processing a file, log: `[START] Processing <filename>` (e.g., `[START] Processing sensor_1.csv`).
   - After computing the result for a file, log: `[DONE] <filename> - Result: <calculated_sum>` (e.g., `[DONE] sensor_1.csv - Result: 1250`).
   - Ensure logging is append-safe or handle race conditions if writing concurrently.

5. **Final Output**:
   - After all files are processed, your script must generate a valid JSON file at `/home/user/results.json`.
   - The JSON should be a single object where the keys are the **filenames** (e.g., `"sensor_1.csv"`) and the values are the calculated sums (integers).
   - Example format:
     ```json
     {
       "sensor_1.csv": 1250,
       "sensor_2.csv": 0,
       "sensor_3.csv": 45
     }
     ```

Make sure your script is executable and actually run it to produce `/home/user/pipeline.log` and `/home/user/results.json` before completing the task.
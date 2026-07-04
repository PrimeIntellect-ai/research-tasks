You are an automation specialist building a data processing pipeline for a network of environmental sensors. The raw data logs are messy and need to be cleaned, gap-filled, and sampled for a downstream machine learning model.

Your task is to implement this pipeline primarily in C, with some bash scripting.

**Step 1: Data Cleaning and Resampling (C Program)**
Write a C program at `/home/user/clean_resample.c` and compile it to `/home/user/clean_resample`.
The program should take two arguments: the input CSV file path and the output CSV file path.
Execution: `./clean_resample /home/user/raw_data.csv /home/user/resampled.csv`

The input CSV (`/home/user/raw_data.csv`) has no header. The format is:
`timestamp,sensor_id,temperature,humidity,notes`

**Rules for processing:**
1. **Line-by-Line Parsing and Dropping:** The `notes` field sometimes contains embedded newlines, which breaks simple line-by-line parsing. You must read the file line-by-line using standard newline characters (`\n`). If a parsed line does not contain exactly 5 fields (4 commas), silently drop it.
2. **Feature Extraction:** You only care about `timestamp` (long), `temperature` (float), and `humidity` (float).
3. **Resampling & Gap-Filling:** The raw data has irregular timestamps. You need to produce output rows at exactly 60-second intervals. 
   - The first output row must start at the timestamp of the *first valid* row in the input.
   - The last output row must not exceed the timestamp of the *last valid* row.
   - For each 60-second interval (e.g., T, T+60, T+120...), output the timestamp, the most recently observed valid temperature, and the most recently observed valid humidity (Forward-Fill). 
   - If multiple valid readings fall within the same 60-second window, use the latest one that occurred *before or at* the target timestamp. (Update your current state as you read through the file).
   
Output format for `resampled.csv`:
`timestamp,temperature,humidity` (floats should be formatted to 1 decimal place, e.g., `%.1f`).

**Step 2: Stratified Sampling (Bash Script)**
Write a bash script at `/home/user/stratify.sh` that takes `/home/user/resampled.csv` as input and produces `/home/user/stratified.csv`.
The machine learning team needs exactly the *first 3* chronologically occurring records from `resampled.csv` for each of the following temperature strata:
- Cold: `< 20.0`
- Moderate: `>= 20.0` and `< 30.0`
- Hot: `>= 30.0`

The final `/home/user/stratified.csv` should contain exactly 9 lines (3 from Cold, followed by 3 from Moderate, followed by 3 from Hot), preserving chronological order within each stratum.

**Initial Setup**
The raw data file is located at `/home/user/raw_data.csv`. Do not modify this file.
Once you have created the files and run your pipeline successfully, you are done.
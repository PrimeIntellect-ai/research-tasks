You are tasked with analyzing a time series of configuration size changes across our server fleet. The data is stored in a simulated remote archive, but the export process corrupted some of the logs by generating invalid unicode escape sequences.

Your objective is to build a robust data processing pipeline that transfers the data, cleans the corrupted JSON, imputes missing time steps, and processes the files in parallel.

**Step 1: Data Transfer**
Copy all `.jsonl` files from `/home/user/remote_archive/` to your working directory `/home/user/workspace/data/`.

**Step 2: Normalization & Parsing (Python)**
The JSON-lines files contain records like this:
`{"timestamp": "2023-11-01T00:00:00Z", "size_bytes": 1050, "message": "Updated conf \u12GZ"}`
The `message` field often contains malformed unicode escapes (like `\u12GZ`) that will cause standard `json.loads()` to crash.
Write a Python script (`/home/user/workspace/process_log.py`) that reads a single JSONL file, safely extracts the `timestamp` and `size_bytes` fields (bypassing or fixing the broken unicode in the string), and creates a pandas DataFrame.

**Step 3: Imputation (Python)**
In the same Python script, convert the `timestamp` column to datetime, set it as the index, and resample the data to an **hourly** frequency (`1H`). 
Use **linear interpolation** to fill in any missing `size_bytes` values for the missing hours.
The script should output the processed data to a CSV file in `/home/user/workspace/processed/` with the same base name as the input file but a `.csv` extension. The CSV should have two columns: `timestamp` (ISO 8601 format, e.g., `2023-11-01T01:00:00Z`) and `size_bytes` (rounded to 1 decimal place).

**Step 4: Parallel Orchestration (Bash)**
Write a bash script `/home/user/workspace/run_pipeline.sh` that acts as a simple DAG:
1. It executes your Python script on all copied `.jsonl` files **in parallel** (using bash background jobs `&` and `wait`, or tools like `xargs -P`).
2. After all files are processed, it merges all the resulting CSV files into a single file.
3. It sorts the final merged data chronologically by timestamp and saves it to `/home/user/workspace/final_series.csv`. The final CSV must include a header: `timestamp,size_bytes`.

**Requirements:**
- Do not use root/sudo privileges.
- Ensure `/home/user/workspace/final_series.csv` exactly matches the expected interpolated time series.
- Handle the broken JSON robustly without dropping entire rows just because the `message` field is malformed.
You are an automation specialist tasked with building a robust, parallelized ETL pipeline to process incoming telemetry data before it is ingested by an aging proprietary system. 

We receive telemetry in CSV format (`timestamp_sec,sensor_name,reading`). However, the upstream systems are unreliable: some files are corrupted, contain malicious shell injections, or trigger buffer overflows in our downstream proprietary ingestor. 

You have access to the legacy ingestor binary at `/app/legacy_processor` (a stripped binary). Through black-box testing, you must deduce its input constraints (e.g., character limits, allowed characters) to build a protective filter.

Your objective is to write two Bash scripts:

1. **The Sanitizer (`/home/user/filter_and_fill.sh`)**
   - Usage: `./filter_and_fill.sh <input_csv>`
   - **Validation Checkpoint:** It must validate the CSV. If the file contains data that would crash or exploit `/app/legacy_processor`, the script must immediately exit with status code `1` and output nothing.
   - **Gap-Filling:** If the file is clean, it must output the data to `STDOUT` (and exit with code `0`). Furthermore, the upstream network frequently drops packets. You must perform forward-fill gap-filling on the `timestamp_sec` column. If timestamps skip seconds (e.g., 100, 101, 104), you must insert rows for 102 and 103 using the `sensor_name` and `reading` from timestamp 101.

2. **The Parallel Batch Processor (`/home/user/batch_process.sh`)**
   - Usage: `./batch_process.sh <input_dir> <output_dir>`
   - It must use standard Bash tools (like `xargs -P` or background jobs) to process all `.csv` files in `<input_dir>` in parallel using `filter_and_fill.sh`.
   - Valid, gap-filled files must be saved in `<output_dir>` with the same filename. Invalid files should be safely ignored (no output file created).

**Constraints:**
- You must write everything in Bash, utilizing shell built-ins, `awk`, `sed`, `grep`, and standard coreutils. Do not use Python, Perl, or other interpreters.
- Clean and evil sample datasets are provided in `/home/user/samples/clean/` and `/home/user/samples/evil/` respectively, to help you test.
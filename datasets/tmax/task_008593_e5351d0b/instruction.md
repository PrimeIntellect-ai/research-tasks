You are an AI assistant helping a researcher organize and backup a messy collection of sensor datasets.

The researcher has a directory located at `/home/user/research_data/raw/` containing various dataset files in CSV, JSON, and XML formats. They need a Python script to parse these files, identify the significant ones, record their statistics, and perform an incremental backup of the new significant datasets.

Write and execute a Python script that performs the following steps:

1. **Parse and Filter:**
   Scan `/home/user/research_data/raw/` for all `.csv`, `.json`, and `.xml` files.
   Calculate the sum of the sensor readings for each file based on its format:
   - **CSV**: Sum the integer values in the `reading` column.
   - **JSON**: The file contains a JSON object with a `readings` key mapped to an array of integers. Sum this array.
   - **XML**: The file contains a root `<data>` element with multiple `<reading>` child elements containing integer text. Sum these values.

   A file is considered **"significant"** if the sum of its readings is **strictly greater than 100**.

2. **Logging:**
   Create a JSON log file at `/home/user/processed_log.json`.
   This file should contain a single JSON object where the keys are the base filenames (e.g., `sensor1.csv`) of ALL **significant** files, and the values are their corresponding calculated sums (as integers).

3. **Incremental Backup:**
   The file `/home/user/last_run.txt` contains a single integer representing a Unix timestamp of the last backup.
   Create a directory at `/home/user/research_data/incremental_backup/` (if it doesn't already exist).
   Copy ONLY the **significant** files whose modification time (mtime) is **strictly greater** than the timestamp in `last_run.txt` into the `/home/user/research_data/incremental_backup/` directory. Do not alter the filenames.

Ensure your Python script runs successfully and leaves the system in the exact state described above.
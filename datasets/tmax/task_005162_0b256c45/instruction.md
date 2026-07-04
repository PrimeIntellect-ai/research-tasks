You are an AI assistant helping a storage administrator manage disk space usage across multiple projects.

The system generates periodic usage reports in JSON format. These reports are placed into the `/home/user/reports/` directory. Due to parallel processing, multiple scripts might attempt to aggregate these reports into a master summary file at the same time.

Your task is to write a Python script at `/home/user/disk_analyzer.py` that processes these reports safely and outputs both a text summary and a binary dump.

**Requirements for `/home/user/disk_analyzer.py`:**

1.  **Parse Reports (Structured Data):**
    Read all `.json` files in `/home/user/reports/`. Each file contains a JSON array of objects with the keys `"project_id"` (an integer) and `"storage_used_mb"` (an integer). Aggregate the total `storage_used_mb` per `project_id`.

2.  **Safe CSV Aggregation (Text I/O & File Locking):**
    Open (or create) `/home/user/project_totals.csv`.
    Because other processes might be accessing this file, you **must** use `fcntl.flock(f, fcntl.LOCK_EX)` to acquire an exclusive lock before reading or writing to it, and release it after (or let it release on close).
    The CSV format should be: `project_id,total_mb`.
    If the CSV already has data, read the existing totals, add the new totals from the current run, and overwrite the file with the updated totals. Sort the output rows by `project_id` in ascending order.

3.  **Binary Dump (Binary I/O):**
    Write the final aggregated results to a binary file at `/home/user/binary_dump.bin`.
    For each project (sorted by `project_id` ascending), write exactly 12 bytes using the Python `struct` module:
    - A 4-byte unsigned integer (Little Endian) for the `project_id`.
    - An 8-byte unsigned integer (Little Endian) for the `total_mb`.
    Format string reference: `<IQ`.

**Actions to take:**
1. Write the Python script `/home/user/disk_analyzer.py` fulfilling the above requirements.
2. Run your script once to process the existing files in `/home/user/reports/` and generate the output files. Ensure the output files exist and are correctly formatted.
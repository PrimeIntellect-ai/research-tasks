You are an operations engineer managing a high-throughput logging cluster. 
A highly active application writes massive JSON log files to `/home/user/active_logs/`. These logs are rotated and deleted continuously, creating a severe race condition if you try to read them directly while archiving.

Your goal is to safely extract all critical errors into a compressed backup format using a provided vendored library.

1. **Environment Setup & Package Fix:**
   We have vendored the `ijson` (version 3.2.3) package at `/app/ijson-3.2.3` because standard `json` module runs out of memory on our large files. However, the vendored version has a deliberate configuration error that forces it to use the pure-Python backend, which is too slow for our strict performance limits. 
   - Identify the perturbation in the package's build/setup configuration that disables the C-extension (`yajl2`).
   - Fix the package, ensure system dependencies for `yajl` are met (if needed, use `apt-get` as sudo is not required for standard user space if headers are there, but assume you might need to install `libyajl-dev` if you have sudo. Wait, you do not have root access. Assume `libyajl-dev` is already installed on the system).
   - Install the fixed package into your Python environment.

2. **Snapshot and Backup Script:**
   Write a Python script at `/home/user/backup_errors.py` that performs the following steps:
   - Perform a "snapshot" of all `.json` files currently in `/home/user/active_logs/` by creating **hard links** to them in `/home/user/backup_staging/`. This avoids the log rotation race condition by freezing the inodes.
   - Iterate through the hard-linked `.json` files. The logs are arrays of JSON objects.
   - Use the `ijson` library to stream-parse the files and find all objects where the `"level"` key is exactly `"CRITICAL"`.
   - Write these critical log entries into a CSV file at `/home/user/critical_logs.csv` with the headers: `timestamp,service,message`.
   - The script must take no arguments and automatically process whatever files are in the staging directory.

3. **Performance Constraint:**
   Your script must be highly optimized. The automated verifier will place a massive (~500MB) JSON file into `/home/user/active_logs/` and execute your `/home/user/backup_errors.py` script. 
   - Your script must complete the snapshotting, parsing, and CSV generation in **under 4.0 seconds**.
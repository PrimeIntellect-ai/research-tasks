You are a DevOps engineer responding to an alert about a crashed legacy metrics service. The service left behind a partial memory dump, a compiled Python file, and a database in an unclean state. 

Your objective is to recover the data, extract the missing configuration from memory, reverse-engineer the broken logic, and produce the correct metric.

All relevant files are located in `/home/user/metrics_service/`.

**Step 1: Database Recovery**
The service was writing to an SQLite database (`data.db`). Due to the crash, uncommitted records are left in the Write-Ahead Log (`data.db-wal`). 
- Force the SQLite database to recover and integrate the WAL file so that all records in the `measurements` table are accessible directly from `data.db`.

**Step 2: Memory Dump Analysis**
The configuration file was lost, but the process memory was dumped to `/home/user/metrics_service/memory.dump`.
- Analyze the binary memory dump to find the secret multiplier. It is stored as a cleartext string in the format `SECRET_MULTIPLIER=<integer>`. Extract this integer.

**Step 3: Reverse Engineering and Formula Correction**
The logic for calculating the metric is in a compiled Python 3 bytecode file `/home/user/metrics_service/calculator.pyc`.
- Decompile or inspect `calculator.pyc` to understand how it queries the database and processes the data.
- You will notice the formula implemented in `calculate_metric(db_path, multiplier)` is incorrect. The original developer mistakenly added the multiplier to the sum of the values.
- **The correct formula is:** The sum of all `value`s in the `measurements` table *multiplied* by the secret multiplier.

**Step 4: Final Calculation**
Write a script at `/home/user/metrics_service/solve.py` that implements the *correct* logic. 
Run your script to calculate the final correct metric using the recovered database and the extracted multiplier.
Write the final calculated number (as a standard string, e.g., "12345.6") to `/home/user/metrics_service/final_metric.txt`.

*Note: You may use standard Linux command-line tools (like `strings`, `sqlite3`, `uncompyle6`, `decompyle3`, or Python's `dis` module) to analyze the files.*
Hello, I'm a DevOps engineer dealing with a critical outage. Our proprietary telemetry aggregator, located at `/app/telemetry_aggregator`, crashed abruptly during a major traffic spike. We need to recover the lost telemetry metrics for our billing system. 

When the system crashed, it left behind three artifacts in the `/home/user/` directory:
1. `telemetry.db` - A corrupted SQLite database.
2. `telemetry.db-wal` - The Write-Ahead Log containing the uncheckpointed metrics from right before the crash.
3. `crash.dmp` - A raw memory dump of the aggregator process at the time of the crash.

The aggregator works by reading raw metrics, applying a dynamic floating-point calibration multiplier, and inserting them into the database. Because of the crash, the final records in the WAL were written *without* the calibration multiplier applied (they suffered precision/scaling loss), and the database was left in a corrupted state that standard clients refuse to read.

Your task is to:
1. **Analyze the Memory Dump:** Inspect `/home/user/crash.dmp` to find the lost dynamic calibration multiplier. The binary stores this in memory as a high-precision float string immediately following the text marker `"CALIBRATION_FACTOR_SCALAR:"`.
2. **Recover the Database:** Salvage the records from the corrupted SQLite database and its WAL file. You need to extract the `timestamp` and `value` fields for all records. (The table schema was `metrics(timestamp TEXT, value REAL)`).
3. **Repair the Precision Data:** Write a pure Bash script (using standard CLI tools like `awk`, `sed`, `bc`, etc.) at `/home/user/repair_metrics.sh`. This script should process your recovered records, multiply every `value` by the calibration multiplier you found in the memory dump, and output a CSV file at `/home/user/recovered_metrics.csv`.

**Output Requirements:**
- The final file must be located exactly at `/home/user/recovered_metrics.csv`.
- The CSV must have the header `timestamp,value`.
- The values must be floating-point numbers corrected by the multiplier.
- Do not use Python, Ruby, or Perl for the data processing script; rely entirely on Bash and POSIX utilities.

Our automated system will grade the accuracy of your `/home/user/recovered_metrics.csv` by calculating the Mean Squared Error (MSE) of the `value` column against our known good reference data. You must achieve high precision to pass.
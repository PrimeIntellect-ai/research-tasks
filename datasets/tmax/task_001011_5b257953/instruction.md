You are a support engineer collecting and analyzing diagnostics from a distributed data pipeline. The system processes metrics from various containerized workers, but the diagnostic pipeline is currently broken.

Your task has two parts:

**Part 1: Fix the Extraction Pipeline**
We use a script `/home/user/collect_diagnostics.py` to concurrently fetch logs from the workers. This script relies on a vendored version of the `sh` library located at `/app/vendored/sh-1.14.3`. 
Currently, `collect_diagnostics.py` crashes randomly with concurrency errors and fails completely when processing containers that output logs with spaces in their filenames. 
You must debug and fix the vendored `/app/vendored/sh-1.14.3/sh.py` package. You cannot replace the package with a downloaded version; you must patch the source code directly so that `collect_diagnostics.py` completes without errors and correctly writes the raw log files into `/home/user/raw_logs/`.

**Part 2: Build a Log Sanitizer**
Once extracted, we discovered that some logs contain "poisoned" metric data. These poisoned logs cause our downstream aggregators to suffer from numerical instability (producing `NaN`s, `Inf`s, or triggering `OverflowError`s during variance calculations).

You must write a classification script at `/home/user/sanitizer.py` that analyzes a single metric log file and determines if it is safe to process.
The script must take exactly one argument (the path to the log file):
`python3 /home/user/sanitizer.py <path_to_log_file.csv>`

Requirements for `sanitizer.py`:
- It must read the CSV file.
- It must exit with status code `0` if the log is perfectly clean and stable.
- It must exit with status code `1` if the log contains any data that would trigger numerical instability (e.g., hidden NaNs, infinities, or values that overflow standard 64-bit floating point representations).
- It must be robust enough to handle large files efficiently.

You can test your script against the logs successfully extracted in Part 1. When you are finished, ensure `/home/user/sanitizer.py` is executable and ready for automated testing.
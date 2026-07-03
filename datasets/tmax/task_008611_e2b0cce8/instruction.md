You are a support engineer tasked with collecting diagnostics for a failing data pipeline. A customer reported that their Python data processing script crashes unpredictably with a `ZeroDivisionError`. 

Through preliminary investigation, we know that the root cause is a **precision loss/underflow issue**. The script reads scientific measurements from a CSV file located at `/home/user/measurements.csv`. One of the measurement records contains a valid non-zero numerical string, but it represents a number so small that it underflows to exactly `0.0` when parsed as a standard 64-bit float in Python. When this `0.0` is passed to the downstream transformation function (which normalizes data by dividing by the measurement), the script crashes.

Your task is to identify the corrupted input causing this precision loss.

1. Analyze `/home/user/measurements.csv`. The file has a header (`id,value`) followed by thousands of data rows.
2. Find the 0-indexed row number (where the first data row immediately after the header is row 0) where the `value` string represents a mathematically non-zero number, but parses to `0.0` in Python.
3. Write a diagnostic summary to `/home/user/diagnostic_report.txt`. The file must contain exactly one line in the following format:
   `Corrupted Row: <row_index>`

You can use Bash commands or write a Python script to isolate the issue. Be exact in your output format.
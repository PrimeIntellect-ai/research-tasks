You are an IT support technician handling an escalated ticket (Ticket #882). 

The nightly data build pipeline is failing. The python build script `/home/user/scripts/build_report.py` aggregates query logs from `/home/user/data/query_logs.csv` into a JSON summary report. However, upstream ingestion issues have introduced corrupted input into the CSV, causing the build script to crash.

Your task is to debug the failure, recover the uncorrupted data, and report the offending queries.

Specifically, you must:
1. Diagnose the build failure by running the Python script on the original CSV data.
2. Identify the corrupted row(s) in `/home/user/data/query_logs.csv` that cause the script to fail. 
3. Create a cleaned version of the data at `/home/user/data/query_logs_fixed.csv` that contains only the valid rows (including the header).
4. Extract the `QueryID` (the first column) of all corrupted/failing rows and save them to `/home/user/bad_queries.log`, one per line, sorted alphabetically.
5. Verify your fix by running `python3 /home/user/scripts/build_report.py /home/user/data/query_logs_fixed.csv` successfully.

Do not modify `/home/user/scripts/build_report.py`. You must resolve the issue strictly by isolating and removing the corrupted data rows from the input.
You are an automation specialist building a robust data processing pipeline. We have a multi-service environment running locally that mimics a remote sensor network.

The environment (which is already running or can be started via `/app/start_services.sh`) consists of:
1. **Data Server**: An HTTP server on `127.0.0.1:8080` serving raw CSV data files.
2. **Stats Accumulator**: A TCP service on `127.0.0.1:9090` that collects summary statistics.

Your goal is to build a C++ data validator and a bash workflow script to process the data.

### Step 1: C++ Data Validator
Create a C++ program at `/home/user/processor.cpp` and compile it to `/home/user/processor`.
The program must take a single file path as an argument: `./processor <filepath>`
It must read the CSV file (which has no header) and validate every row against these strict constraints:
- Column 1 (`id`): Exactly 8 lowercase hexadecimal characters.
- Column 2 (`sensor_id`): Integer between 1 and 999 (inclusive).
- Column 3 (`temperature`): Float between -50.0 and 150.0 (inclusive).
- Column 4 (`timestamp`): Integer representing UNIX time, must be between 1600000000 and 1700000000 (inclusive).
- Column 5 (`active`): Exactly the string "true" or "false".

If **all** rows in the file are valid, the program must print `VALID` to standard output and exit with status code `0`.
If **any** row violates any constraint, or if the file format is incorrect, the program must print `INVALID` to standard output and exit with status code `1`.

### Step 2: Automation Workflow
Create a bash script at `/home/user/process_all.sh` that orchestrates the pipeline:
1. Fetch the list of available files by doing a GET request to `http://127.0.0.1:8080/files.list`.
2. For each filename in the list:
   - Download the file from `http://127.0.0.1:8080/data/<filename>` to a local temporary directory.
   - Run your compiled `./processor` on the downloaded file.
   - If the file is `VALID` (exit code 0), calculate the average `temperature` of all rows where `active` is `true`. (You can do this using standard bash tools like `awk` or extend your C++ program to output it—your choice, as long as it's accurate to 2 decimal places).
   - Send the result to the Stats Accumulator by sending a TCP message in the exact format: `<filename>:<average_temp>\n` to `127.0.0.1` port `9090`. (e.g., `sensor_data_1.csv:45.21`). Do not send anything if the file is invalid.

Make sure `/home/user/process_all.sh` is executable. You may use standard shell built-ins, coreutils, `curl`, `nc`, `awk`, etc.
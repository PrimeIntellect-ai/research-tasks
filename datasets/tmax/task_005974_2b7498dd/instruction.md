You are a log analyst tasked with investigating authentication failures from a legacy system. You need to parse a custom log file, extract and validate specific fields, normalize the data, aggregate it into time buckets, and set up a scheduled pipeline to automate this process.

Your primary tool for parsing and processing the data must be a C program.

**1. Input Data**
You have a log file located at `/home/user/auth_sys.log`.
The logs have the following format:
`[YYYY-MM-DD HH:MM:SS] Event: <EVENT_TYPE> User: <Username> IP: <IP_Address> Msg: <Message...>`

Example:
`[2023-10-24 14:35:12] Event: FAILED_LOGIN User: Admin_2 IP: 192.168.1.50 Msg: Bad password`

**2. Data Processing Requirements (C Program)**
Write a C program at `/home/user/parser.c` that reads `/home/user/auth_sys.log` and performs the following:
*   **Tokenization & Filtering:** Extract only the lines where `Event: FAILED_LOGIN`. Ignore all other events.
*   **Time-based Bucketing:** Extract the timestamp and round it down to the nearest hour (e.g., `2023-10-24 14:35:12` becomes the bucket `2023-10-24 14:00:00`).
*   **Constraint-based Validation:** 
    *   The `Username` must consist of exactly 3 to 15 characters, containing only letters, numbers, and underscores (`A-Z`, `a-z`, `0-9`, `_`). 
    *   The `IP_Address` must match a basic IPv4 pattern: 1 to 3 digits, followed by a dot, repeated 3 times, ending with 1 to 3 digits (e.g., `10.0.0.1` is valid, `10.0.0.1.5` is invalid, `abc.def.ghi.jkl` is invalid). You may use POSIX regex (`<regex.h>`) for validation.
    *   *Skip/ignore any log lines that fail these validations.*
*   **Normalization:** Convert the extracted valid `Username` to strictly lowercase.
*   **Aggregation:** Count the number of failed login attempts for each unique combination of `(Time_Bucket, IP_Address, Normalized_Username)`.

**3. Output Requirements**
The C program should write the aggregated results to `/home/user/hourly_failures.csv`.
*   Format: `Time_Bucket,IP_Address,Normalized_Username,Failure_Count`
*   The output must be sorted chronologically by `Time_Bucket`. If there are ties, sort alphabetically by `IP_Address`, then alphabetically by `Normalized_Username`.

**4. Pipeline Scheduling**
*   Create a bash script at `/home/user/run_parser.sh` that compiles `/home/user/parser.c` (if not already compiled) to an executable `/home/user/parser` and runs it. The script must have executable permissions.
*   Create a crontab configuration file at `/home/user/log_cron`. It should contain the exact cron expression to execute `/home/user/run_parser.sh` at minute 0 past every hour (the top of the hour).

Ensure your C program is robust and correctly handles the specified constraints. Run your bash script to generate the final `/home/user/hourly_failures.csv` file.
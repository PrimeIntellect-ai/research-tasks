You are a Site Reliability Engineer (SRE) investigating an uptime monitoring system that has been reporting inconsistent metrics. 

Your team relies on a Python script located at `/home/user/app/aggregator.py` to calculate the total system uptime from log files. However, you've noticed two major issues:
1. The logging system crashed and dumped its raw memory to a binary file at `/home/user/app/crash_dump.bin`. The plain text logs are trapped inside this binary blob, surrounded by non-printable garbage bytes.
2. Even when fed with valid text logs, `aggregator.py` sometimes reports different total uptime values for the exact same input file due to a severe concurrency bug.

Your tasks are:
1. Extract the human-readable log lines from `/home/user/app/crash_dump.bin` and save them to a plain text file at `/home/user/app/recovered_logs.txt`. The valid log lines you care about always contain the string `UPTIME_PING=`.
2. Analyze and debug `/home/user/app/aggregator.py`. Identify the race condition that causes the total uptime calculation to be non-deterministic, and fix the code so it safely handles concurrent updates.
3. Run your fixed `aggregator.py` against `recovered_logs.txt` and pipe the standard output to `/home/user/final_metric.txt`.

The automated test will verify that `/home/user/final_metric.txt` contains the correct and consistent total uptime string (e.g., `Total Uptime: XXXXX`). Do not change the standard output format of the print statement in the Python script.
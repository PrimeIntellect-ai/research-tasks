You are an on-call engineer responding to a critical 3 AM page. The nightly log processing pipeline has failed, halting the generation of the daily security report.

You log into the server and find the pipeline files in `/home/user/pipeline`. The pipeline is orchestrated by a shell script `build.sh`, which prepares an SQLite database from a CSV export and then runs a Python script `parser.py` to cross-reference log events with the database.

Currently, running `./build.sh` fails. There appear to be multiple issues across the build step, the log parsing logic, and the database query logic.

Your task:
1. Diagnose and fix the build failure in `build.sh`.
2. Fix the edge-case parsing crash in `parser.py`.
3. Debug and fix the query logic in `parser.py` so it correctly identifies the active users.

When all bugs are resolved, running `/home/user/pipeline/build.sh` should execute cleanly without errors and generate a `/home/user/pipeline/report.txt` file containing the correct list of active users found in the logs.

Do not change the names of the generated files or the expected output format in the report. Fix the underlying bugs rather than hardcoding the final output.
You are a DevOps engineer tasked with debugging a data processing application. The application is supposed to run via a bash script, process data from an SQLite database, and output the results to a JSON file. However, the build is failing, the script crashes when it does run, and the final query results are incorrect.

The application directory is located at `/home/user/app`.

Here is what you need to do:
1. **Build Failure Diagnosis**: The script `/home/user/app/run.sh` attempts to create a virtual environment, install dependencies from `/home/user/app/requirements.txt`, and run the Python application. The dependency installation is currently failing. Identify and fix the issue in `requirements.txt` so that the installation succeeds.
2. **Container/Log Inspection & Intermediate State Tracing**: Once the build succeeds, the application `/home/user/app/src/process_data.py` crashes during execution. Inspect the log file generated at `/home/user/app/logs/process.log` to trace the intermediate state and understand why it is crashing. Fix the Python code to prevent the crash.
3. **Query Result Debugging**: The Python script is supposed to fetch "active" users and their total transaction amounts, filtering out anyone whose total transaction amount is 0 or null, and then save the output to `/home/user/app/output/results.json`. Additionally, the output list must be sorted in **descending order** based on the total amount. The current SQL query and Python logic are flawed and do not meet these requirements. Fix the query and/or Python code.

The final output in `/home/user/app/output/results.json` should be a strictly formatted JSON array of dictionaries, where each dictionary has the keys `"name"` and `"total"`.

Example of expected output format:
```json
[
  {"name": "Alice", "total": 150.5},
  {"name": "Bob", "total": 45.0}
]
```

Run `/home/user/app/run.sh` to test your changes. You have successfully completed the task when `run.sh` executes without errors and the correct results are written to `results.json`.
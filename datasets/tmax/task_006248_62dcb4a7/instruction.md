You are a system administrator maintaining a server without root privileges. A previous process manager crashed, leaving behind a dirty state file. You need to identify failed container services from a system file, and write a custom Python supervisor script to inject their required environment variables and attempt to restart them.

Step 1: Text Processing
There is a file located at `/home/user/service_mounts.txt`. It contains lines with mixed service statuses. The columns are separated by arbitrary amounts of whitespace.
The format is: `<service_name> <type> <status> <env_var> <command>`
Lines starting with `#` are comments.

Use standard shell text processing tools (e.g., awk, grep, sed) to extract only the services where the `<type>` is `CONTAINER` and `<status>` is `FAILED`. 
Save the extracted lines into `/home/user/parsed_services.csv` with exactly this comma-separated format:
`service_name,env_var,command`

Step 2: Python Supervisor
Write a Python script at `/home/user/container_supervisor.py`. This script must:
1. Read `/home/user/parsed_services.csv`.
2. For each line, parse the service name, environment variable string (e.g., `KEY=VALUE`), and command.
3. Use the Python `subprocess` module to execute the `<command>`. 
   - You MUST inject the parsed environment variable into the subprocess's environment (in addition to the current environment variables, or at least the specific one required).
4. Wait for the process to finish. If the process exits with a non-zero exit code, your supervisor must attempt to restart the process exactly ONE more time.
5. After the executions (either succeeding on the first try, succeeding on the second try, or failing both tries), log the final outcome for that service to `/home/user/supervisor.log`.

The format for `/home/user/supervisor.log` must be exactly one line per parsed service in the order they appear in the CSV:
`[<service_name>] SUCCESS` (if it exited with code 0 on the first or second try)
`[<service_name>] FAILED` (if it exited with a non-zero code on the second try)

Step 3: Execution
Run your Python script so that the log file is generated. Do not manually modify the mock scripts.
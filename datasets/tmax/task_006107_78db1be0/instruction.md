As an observability engineer, you need to configure a local storage monitoring pipeline to ensure large data artifacts are not accidentally committed to our dashboard configurations, and that storage metrics are periodically logged.

Please complete the following tasks:

1. Write a Python script at `/home/user/generate_metric.py`. This script must calculate the total size (in bytes) of all files inside the directory `/home/user/data_dir` (including subdirectories). 
   - Every time the script runs, it must append a single line to `/home/user/dashboard.log` in exactly this format: `METRIC: <total_bytes_size>`.
   - If the total calculated size is strictly greater than `5000` bytes, the script must exit with a status code of `1`. Otherwise, it must exit with a status code of `0`.

2. Configure a Git `pre-commit` hook in the existing repository located at `/home/user/dash_repo`. 
   - The hook must execute `/home/user/generate_metric.py`.
   - The hook must enforce the Python script's exit code, effectively blocking the Git commit if the data directory size exceeds 5000 bytes.

3. Schedule a cron job for the current user that executes `/home/user/generate_metric.py` exactly every 5 minutes. Use standard cron syntax.

Ensure all file paths are exact, scripts are executable where necessary, and the python script runs flawlessly.
You are acting as a capacity planner for our infrastructure team. We have a broken telemetry environment and need to extract resource usage forecasts. Our monitoring stack consists of three services running under `/app/`:
1. `log_generator.py`: Writes mock resource usage logs to a directory.
2. `telemetry_api.py`: A Python Flask service on port 5000 that exposes the latest metrics.
3. `prom_scraper.sh`: A simple bash daemon that curls the Flask API every second and dumps the output.

Currently, the services are failing because the environment is not set up, and we are missing our core forecasting script.

Please complete the following tasks:

1. **Environment Setup (Idempotent Scripting & Directory Management):**
   Write a bash script at `/home/user/setup_env.sh` that idempotently:
   - Creates a local group called `cap-planners` and a user `cap-worker` (use mock user/group creation in `/home/user/passwd_mock` and `/home/user/group_mock` files, adhering to standard `/etc/passwd` format, since you lack root access).
   - Creates the directory `/home/user/telemetry_data` and a symlink to it at `/home/user/telemetry_link`.
   - Writes a properly formatted `fstab` entry into `/home/user/mock_fstab` that would mount a `tmpfs` to `/home/user/telemetry_data` with a size of 100M and belonging to the `cap-planners` mock group.

2. **Service Composition (Glue):**
   The `log_generator.py` is hardcoded to write to `/var/log/telemetry/usage.log`, which you cannot write to. 
   Configure the environment so that `log_generator.py` (which reads the `LOG_PATH` environment variable) and `telemetry_api.py` (which reads the `DATA_SOURCE` environment variable) both point to `/home/user/telemetry_link/usage.log`. Start both processes in the background so that `prom_scraper.sh` successfully logs output to `/home/user/scraper_output.log`.

3. **Forecast Calculator (Python implementation):**
   We have a compiled binary at `/app/oracle_forecaster` that calculates capacity scores from log lines. We lost the source code.
   Write a Python script at `/home/user/forecast_calc.py` that takes a single command-line argument (a log line like `"CPU:85 MEM:1024 IO:50"`) and prints the calculated capacity score to standard output.
   Your Python script must perfectly match the output of `/app/oracle_forecaster` for any valid input. Reverse-engineer the mathematical relationship by querying `/app/oracle_forecaster`. Ensure your script has exactly this entry point: `python3 /home/user/forecast_calc.py "<log_line>"`.

Ensure your services are running and your `forecast_calc.py` is strictly equivalent to the oracle before finishing.
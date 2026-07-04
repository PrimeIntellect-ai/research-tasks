You are an engineer troubleshooting a locally-run CI/CD pipeline that processes data. The pipeline uses a custom, lightweight Python-based process supervisor to manage concurrent tasks, but it is currently failing. 

The process supervisor (`/home/user/project/supervisor.py`) reads a configuration file (`/home/user/project/services.ini`) to start services. Currently, `analytics-worker` frequently crashes because it tries to read a filesystem path before `data-fetcher` has finished creating it. This simulates a classic `systemd` issue where a service fails due to a missing `After=` dependency.

Your objective is to fix the pipeline, ensure robust filesystem handling, and wrap it in a reliable CI script.

Perform the following tasks:

1. **Fix the Startup Order:**
   Edit `/home/user/project/services.ini`. Add an `After=data-fetcher` directive under the `[analytics-worker]` section so the supervisor knows to wait for `data-fetcher` to complete its initialization phase before starting `analytics-worker`.

2. **Implement Robust Error Handling:**
   Even with proper ordering, filesystem I/O can sometimes lag. Edit `/home/user/project/analytics-worker.py`. Update the script so that when it attempts to open `/home/user/project/data/metrics.csv`, it uses a retry mechanism. It must:
   - Attempt to open the file.
   - If the file does not exist, catch the specific exception, wait 1 second, and retry.
   - It must retry a maximum of 3 times (i.e., 4 total attempts).
   - If it still fails after the retries, it should exit with code 1.

3. **Construct the CI/CD Wrapper Script:**
   Create a bash script at `/home/user/project/run_pipeline.sh` with the following requirements:
   - Ensure the directory `/home/user/project/data` is empty before starting (clean up any previous runs).
   - Ensure the directory `/home/user/project/logs` exists.
   - Execute the supervisor script: `python3 /home/user/project/supervisor.py`
   - Redirect both stdout and stderr of the supervisor to `/home/user/project/logs/pipeline.log`.
   - If the supervisor exits with a successful exit code (0), write the exact string `PIPELINE_SUCCESS` to `/home/user/project/status.txt`. If it fails, write `PIPELINE_FAILED` to the same file.
   - Make sure `run_pipeline.sh` is executable.

Note: All necessary scripts and configuration files already exist in `/home/user/project/` except for `run_pipeline.sh` and the directories you need to manage in step 3.
You are an observability engineer tasked with tuning and building a custom local dashboard feed. You need to configure the environment, set up a dummy service, and write a Python metric collector that monitors storage and process health.

Please complete the following steps exactly as specified. All work should be done within `/home/user`.

**Phase 1: Environment and Process Setup**
1. Create a shell profile script at `/home/user/.obs_profile`. In this file, export two environment variables:
   - `OBS_MAX_DISK_KB=1000`
   - `OBS_PROC_NAME=obs_target.py`
2. Create a dummy target service. Write a Python script at `/home/user/obs_target.py` that simply loops infinitely and sleeps (e.g., `import time; while True: time.sleep(1)`). Start this script in the background so it remains running.
3. Create a directory named `/home/user/data_dir`. Generate a 2 Megabyte dummy file inside it named `/home/user/data_dir/dummy.dat` (exactly 2048 KB).
4. Create a directory for your logs at `/home/user/dashboard_logs`. Ensure this directory has restrictive permissions: only the owner should have read, write, and execute permissions, and the group should have only read and execute permissions (no permissions for others).

**Phase 2: Metric Collector Script**
Write a Python script at `/home/user/collector.py`. The script must do the following:
1. Read the environment variables `OBS_MAX_DISK_KB` and `OBS_PROC_NAME` (assume they are loaded into the environment when the script is run).
2. Monitor the process: Find the Process ID (PID) of the running script matching `OBS_PROC_NAME`. 
3. Monitor storage: Calculate the total disk size of the `/home/user/data_dir` directory in Kilobytes (KB). (For a 2MB file, this should be 2048 KB).
4. Determine if the disk quota is exceeded: `quota_exceeded` should be `true` if the calculated KB is strictly greater than `OBS_MAX_DISK_KB`, and `false` otherwise.
5. Write these metrics to a JSON file at `/home/user/dashboard_logs/metrics.json`. The JSON file must have exactly this schema:
   ```json
   {
     "target_pid": <integer PID of the process>,
     "target_status": "running",
     "data_dir_kb": <integer size in KB>,
     "quota_exceeded": <boolean>
   }
   ```

**Phase 3: Execution**
Ensure the `obs_target.py` process is running in the background. Then, execute your collector script (making sure the environment variables from `/home/user/.obs_profile` are loaded into the environment of the collector script) to generate the `/home/user/dashboard_logs/metrics.json` file.
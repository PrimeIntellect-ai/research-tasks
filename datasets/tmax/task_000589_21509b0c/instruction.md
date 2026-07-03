You are an observability engineer tuning the dashboard metrics pipeline for our new application. We have a custom log-parsing metrics exporter vendored at `/app/fast-metric-exporter`. It is designed to parse access logs and aggregate throughput metrics, but it is currently failing in production and is far too slow to handle our log volume.

Your task is to fix the exporter, configure the host environment, and set up a user-level background service to run it.

Here are your specific requirements:

1. **Fix the Vendored Package**: The source code at `/app/fast-metric-exporter` is supposed to use a compiled Cython extension (`parser.pyx`) for high-performance log parsing. However, a recent commit accidentally broke the build configuration in `setup.py`. Identify the perturbation, fix `setup.py`, and build/install the package locally for the `user`. 

2. **Locale and Timezone**: The application logs are generated using the `Asia/Tokyo` timezone, but the parser crashes if the system timezone doesn't match the log timezone. You must configure the environment so the exporter correctly interprets these timestamps without modifying the Python source code of the parser itself.

3. **Permission and ACL Management**: The logs are located in `/home/user/app_logs`. Ensure that the directory has strict ACLs: the owner (`user`) must have read/write access, but you must set a default ACL ensuring any new files created in this directory automatically get `r--` permissions for the user `user` (to prevent accidental modifications by other scripts).

4. **Process & Service Management**: Create a systemd user service named `fast-exporter.service`. 
   - It should execute the installed `fast-metric-exporter` binary.
   - It must read from `/home/user/app_logs/input.log`.
   - It must output the aggregated metrics to `/home/user/metrics.json`.
   - Ensure the service configuration file manages the Locale/Timezone requirement mentioned in step 2 (via environment variables in the service config).

5. **Performance Requirement**: After fixing the C-extension build, the service must be able to process a 500,000-line log file in under 3.0 seconds. 

To complete the task:
- Apply your fixes and configurations.
- Start and enable the systemd user service (`fast-exporter.service`).
- Run `systemctl --user start fast-exporter.service` to ensure it works. 
- Create a file `/home/user/solution_ready.txt` when you are done. The automated verifier will trigger the service with a massive test log and measure the end-to-end execution time to verify the performance threshold.
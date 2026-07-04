You are an automated backup operator testing restores for our legacy interactive backup system. 

We have a legacy restore tool located at `/home/user/legacy_restore.sh`. This tool is strictly interactive, relies on specific environment variables, and extracts data to `/home/user/restore_dir`. 

Your task is to fully automate the execution of this tool and monitor the storage usage changes. 

Requirements:
1. Write a script (using `expect`, Python's `pexpect`, or similar) at `/home/user/run_restore.sh` (or `.py`) to interactively drive the `/home/user/legacy_restore.sh` tool.
2. The legacy tool requires the timezone environment variable `TZ` to be set to `Pacific/Honolulu`. Ensure your automation sets this for the execution of the tool.
3. The tool will prompt for two interactive inputs:
   - `Enter backup archive password: ` (You must provide: `V@ult2024`)
   - `Enter target restore date (YYYY-MM-DD): ` (You must provide: `2024-01-01`)
4. To track disk usage (simulating a quota check), your automation must calculate the total size in bytes of the `/home/user/restore_dir` directory **before** and **after** running the legacy tool. Use `du -sb /home/user/restore_dir | cut -f1` to measure this. (Assume the directory exists and is initially empty).
5. Output the storage results to a log file at `/home/user/restore_metrics.log` with exactly the following format:
   ```
   Before: <bytes> bytes
   After: <bytes> bytes
   ```

Do not modify the legacy tool. Complete the task by writing the automation script and running it to produce the `restore_metrics.log` file.
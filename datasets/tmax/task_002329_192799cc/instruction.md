As a capacity planner, I need an automated way to track system memory usage over time to forecast future resource needs. 

Please create a robust Python script and schedule it to run automatically. Here are the specific requirements:

1. Create a Python script at `/home/user/capacity_monitor.py`.
2. The script must read `/proc/meminfo` to calculate the current memory usage percentage. You must use `MemTotal` and `MemAvailable` for the calculation: `Percentage = ((MemTotal - MemAvailable) / MemTotal) * 100`.
3. The script must log this information by appending it to `/home/user/memory_capacity.log`.
4. The log entry must exactly match this format: `YYYY-MM-DD HH:MM:SS | Used: XX.XX%` (where `XX.XX` is the percentage rounded to exactly two decimal places). Use the system's local time.
5. Implement error handling: if `/proc/meminfo` cannot be read or parsed for any reason, the script should catch the exception and instead append `YYYY-MM-DD HH:MM:SS | ERROR: Cannot read meminfo` to the log file.
6. Make the script executable.
7. Schedule this script to run every single minute using the user's crontab. The cron job must use `/usr/bin/python3` explicitly to execute the script.

Please execute the necessary commands to create this script, set its permissions, and configure the cron job.
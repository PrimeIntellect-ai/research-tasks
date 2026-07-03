You are a FinOps analyst tasked with optimizing cloud costs for a simulated container environment. To reduce billing during peak hours, non-essential batch-processing instances need to be scaled down in a staged manner, prioritizing the most expensive instances first.

There is a file located at `/home/user/instances.txt` containing the active instances and their hourly cost in USD, separated by a space.
For example:
```
worker-alpha 1.25
worker-beta 4.50
worker-gamma 0.75
```

Your task is to:
1. Create a Bash script at `/home/user/scale_down.sh` that performs a simulated staged deployment scale-down.
2. The script must read `/home/user/instances.txt` and sort the instances by their hourly cost in descending order (highest cost first).
3. For each instance in the sorted list, the script must append exactly the following line to `/home/user/scale_log.txt`:
   `SHUTTING DOWN: <instance_name> (Cost: <cost>)`
4. The script must be executable.
5. You must also create a text file at `/home/user/finops.cron` containing exactly one line with a valid cron expression and command to execute your `/home/user/scale_down.sh` script at 09:00 AM on every weekday (Monday through Friday). Do not include any other text or comments in this file.

Ensure the exact formats are followed for the log entries and the cron file. You can test your script manually to ensure `/home/user/scale_log.txt` is generated correctly.
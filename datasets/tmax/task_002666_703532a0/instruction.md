You are a log analyst investigating performance patterns across two interconnected microservices. Service A logs CPU usage at regular intervals, while Service B logs memory usage at irregular intervals. To analyze their correlation, you need to build an automated data processing pipeline.

Your task is to write a C program that aligns these logs by timestamp and interpolates missing memory usage values, then orchestrate this as a scheduled pipeline.

Step 1: The C Program
Write a C program located at `/home/user/align_logs.c` and compile it to `/home/user/align_logs`.
The program must read two CSV files:
1. `/home/user/logs/srv_a.log`: Contains `timestamp,cpu_usage`
2. `/home/user/logs/srv_b.log`: Contains `timestamp,mem_usage`

The program must output a new CSV file to `/home/user/output/aligned.csv` with the header: `timestamp,cpu,mem`.
For every timestamp in `srv_a.log`:
- If the timestamp is strictly before the first timestamp in `srv_b.log` or strictly after the last timestamp in `srv_b.log`, drop the record (do not output it).
- Otherwise, use linear interpolation based on the two closest bounding timestamps in `srv_b.log` to estimate the `mem_usage` at Service A's exact timestamp. If Service A's timestamp exactly matches a timestamp in Service B, use that exact memory value.
- Format the output values for `cpu` and `mem` to exactly two decimal places. Timestamps should be integers.

Step 2: The Pipeline Script
Create a bash script at `/home/user/run_pipeline.sh` that:
1. Creates the directory `/home/user/output` if it doesn't exist.
2. Executes `/home/user/align_logs`.
3. Moves `/home/user/logs/srv_a.log` and `/home/user/logs/srv_b.log` to `/home/user/logs/archive/` (create this directory if it doesn't exist).
Make sure the script is executable. Run the script once manually to generate the initial `/home/user/output/aligned.csv`.

Step 3: Scheduling
We want to schedule this pipeline to run automatically. Add a cron job for the current user (`user`) that runs `/home/user/run_pipeline.sh` every hour at minute 15. Do this by configuring the user's crontab.

System details:
- Working directory is `/home/user`.
- Ensure your C code handles basic file I/O safely and assumes timestamps in the inputs are strictly increasing.
You are a FinOps analyst tasked with automating the extraction and organization of cloud cost anomalies from daily billing logs. 

You have a directory `/home/user/billing_logs/` containing daily CSV files named by date (e.g., `2023-10-01.csv`). Each file has the following columns: `date,service,resource_id,cost`.

Please perform the following tasks:

1. **Python Log Processor**: Write a Python script at `/home/user/process_billing.py` that reads all CSV files in `/home/user/billing_logs/`. For any row where the `cost` is strictly greater than `500.00`, append a log entry to `/home/user/finops_output/anomalies.log`. Ensure the output directory exists.
   The log entry must exactly match this format:
   `[<date>] WARNING: High cost anomaly - Service: <service>, Resource: <resource_id>, Cost: $<cost>`
   (Ensure the cost is formatted to exactly 2 decimal places).

2. **Directory and Link Organization**: Write a bash script at `/home/user/organize_links.sh` that processes `/home/user/finops_output/anomalies.log` using text processing tools (like `awk`, `sed`, or `grep`). 
   For each anomaly found in the log:
   - Extract the `date` and `resource_id`.
   - Create a directory for the resource: `/home/user/finops_output/high_cost/<resource_id>/`.
   - Create a symbolic link inside that directory pointing to the original billing CSV file (`/home/user/billing_logs/<date>.csv`). The symlink itself should be named `<date>.csv`.

3. **Log Rotation**: Create a logrotate configuration file at `/home/user/logrotate.conf` to manage `/home/user/finops_output/anomalies.log`. The configuration must specify:
   - Rotate when the file size reaches `1k`
   - Keep exactly `3` rotations
   - Compress the rotated logs
   - Do not error if the file is missing (`missingok`)

4. **Execution**: Run your Python script to generate the anomalies log, and then run your bash script to create the directory structure and symlinks.
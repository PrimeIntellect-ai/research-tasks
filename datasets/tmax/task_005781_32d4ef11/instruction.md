You are a data engineer responsible for building an ETL pipeline to process server logs. 

We have a legacy system that drops a log file at `/home/user/raw_data.log`. This file is encoded in `ISO-8859-1`.
The log file contains pipe-separated values with the following format:
`timestamp | server_name | status_code | message`
The timestamp is in ISO 8601 format (e.g., `2023-10-24T14:23:11Z`).

Your task is to create a Bash script at `/home/user/etl.sh` that performs the following tasks:
1. Reads `/home/user/raw_data.log`.
2. Converts the text from `ISO-8859-1` to `UTF-8`.
3. Extracts the hour from the timestamp (i.e., `YYYY-MM-DDTHH`) and the `status_code`.
4. Groups the data into hourly buckets and counts the number of `500` status codes per hour.
5. Performs simple anomaly detection: if an hour has strictly more than `2` occurrences of the `500` status code, it is considered an anomaly.
6. Writes the anomalies to `/home/user/alerts.csv` in the exact format: `YYYY-MM-DDTHH,count` (sorted chronologically).

After writing the script:
1. Make sure the script is executable.
2. Run the script once manually to generate `/home/user/alerts.csv`.
3. Schedule this script to run automatically at minute 15 of every hour using the current user's crontab. The cron command should be `/bin/bash /home/user/etl.sh`.

Ensure the final `alerts.csv` is correctly formatted and contains only the hours that breached the anomaly threshold.
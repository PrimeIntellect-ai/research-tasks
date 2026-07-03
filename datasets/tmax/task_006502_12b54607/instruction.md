You are a data engineer tasked with building a lightweight, Bash-driven ETL pipeline to process raw system events. 

You have a log file located at `/home/user/raw_events.log`. Each line contains a timestamp, a log level, and a JSON payload. 

Your task is to write a master script at `/home/user/pipeline.sh` that performs the following steps:
1. **Extraction**: Extract the exact string value of the `message` field from the JSON payload on each line.
2. **Hash-based Deduplication**: Deduplicate the extracted messages. Save the MD5 checksums (just the 32-character hex hashes, one per line, sorted alphabetically) of these unique messages to `/home/user/hashes.txt`.
3. **Similarity Filter**: Compare each unique extracted message against the target string `"CRITICAL: DB connection timeout"`. Filter the unique messages, keeping only those that have a Levenshtein distance of 5 or less from the target string. (You may use Python inline or a separate python script called from your Bash script to compute the Levenshtein distance).
4. **Load**: Save the filtered original messages (not the hashes) to `/home/user/alerts.txt`, sorted alphabetically.
5. **Orchestration**: Ensure the script `/home/user/pipeline.sh` correctly pipes or orchestrates data through these stages when executed.
6. **Scheduling**: Write the exact crontab entry (just a single line) that would schedule `/home/user/pipeline.sh` to run every 15 minutes into a file at `/home/user/cronjob.txt`.

Ensure your `pipeline.sh` script has execute permissions and runs successfully, generating the required output files (`hashes.txt` and `alerts.txt`).
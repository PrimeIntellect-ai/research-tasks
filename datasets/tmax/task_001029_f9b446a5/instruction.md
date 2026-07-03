You are a data engineer building a lightweight ETL pipeline. 

Every hour, your system receives a batch of logs in JSON-Lines format at `/home/user/raw_events.jsonl`. Unfortunately, the downstream system generating these logs has a bug: it occasionally emits invalid unicode escape sequences (e.g., `\uZZZZ`), which completely breaks standard JSON parsers like `jq` or `python -m json.tool`.

You need to extract information from these logs and enrich it with user metadata without choking on the malformed JSON. 

Perform the following steps:
1. Write a Bash script at `/home/user/etl.sh`.
2. Inside the script, extract the `user_id` and `event` values from `/home/user/raw_events.jsonl` using standard Linux text processing tools (e.g., `sed`, `awk`, or `grep`), bypassing the need to parse the broken JSON formally.
3. Join the extracted data with the reference file `/home/user/users.csv` on the `user_id` field.
4. The script must write the joined output to `/home/user/output.csv`. The output must be a valid CSV file starting with the header `user_id,event,region,tier`, and the rows must be sorted numerically by `user_id` in ascending order.
5. Make your script executable.
6. Schedule this script to run automatically at the top of every hour (minute 0) by adding it to the user's crontab. Ensure any existing crontab entries (if they exist) are preserved.

*Note: You do not need to wait for the cron job to trigger. Run your script manually once to generate `/home/user/output.csv` so your work can be verified.*
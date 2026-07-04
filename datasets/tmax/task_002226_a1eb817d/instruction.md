You are a log analyst investigating patterns across international servers. Our logs come from different regions, using different timestamp formats, timezones, and character encodings. 

Your task is to write a bash script at `/home/user/parser.sh` that processes these logs, extracts specific features, normalizes the data, and then set it up as a recurring job.

Here is the setup:
You have two log files in `/home/user/incoming/`:
1. `syslog_eu.log`
   - Encoding: ISO-8859-1
   - Format: `[DD/MMM/YYYY:HH:MM:SS +TZ] LEVEL: Message`
   - Example: `[12/Oct/2023:14:32:10 +0200] INFO: Démarrage`

2. `app_asia.log`
   - Encoding: UTF-16LE
   - Format: `YYYY-MM-DD HH:MM:SS TZ - LEVEL - Message`
   - Example: `2023-10-12 21:40:00 JST - OK - 起動`

Your script `/home/user/parser.sh` must do the following:
1. Parse both files and convert their contents to UTF-8.
2. Extract only the lines representing errors (look for the exact strings `ERROR:` in the EU log and `- FAIL -` in the Asia log).
3. Extract the timestamp and convert it to a UNIX Epoch timestamp.
4. Extract the exact error message text (everything after the level indicator and its surrounding spaces).
5. Append the normalized output to `/home/user/extracted_errors.log` in the exact format: `EPOCH_TIMESTAMP|Message`
   (e.g., `1697114100|Connexion échouée`)
6. Sort `/home/user/extracted_errors.log` numerically by the epoch timestamp in-place after processing.

Finally, do two things to complete the task:
1. Run your script once so that `/home/user/extracted_errors.log` is generated.
2. Add a cron job for the `user` account that runs `/home/user/parser.sh` every 5 minutes. (Ensure the crontab is updated).

Ensure the script is executable. Use standard Bash tools (`iconv`, `date`, `awk`, `sed`, `grep`, etc.).
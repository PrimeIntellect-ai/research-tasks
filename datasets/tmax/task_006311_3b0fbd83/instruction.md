I am a cloud architect migrating a legacy application to a new global infrastructure. The legacy application was hosted in Japan, and its log files were written using the local timezone (`Asia/Tokyo`) without specifying the timezone offset. 

I need you to write and execute a Bash script at `/home/user/migrate_logs.sh` to extract the critical errors and standardize the timestamps for our new central logging system.

Here are the exact requirements for your script:
1. Read the legacy log file located at `/home/user/legacy_app.log`.
2. Find all lines that contain the exact string `[CRITICAL]`.
3. For each matching line, extract the timestamp and the message. The original timestamps are in the `Asia/Tokyo` timezone.
4. Convert the timestamp to `UTC` and format it exactly as `%Y-%m-%d %H:%M:%S UTC`.
5. Write the extracted, timezone-converted lines to a new file at `/home/user/critical_utc.log`. The format of each line in the new file must be: `TIMESTAMP | MESSAGE` (where TIMESTAMP is the new UTC timestamp, and MESSAGE is the text following the `[CRITICAL] ` tag).
6. Because these logs contain sensitive crash dumps, you must ensure that `/home/user/critical_utc.log` has strict permissions: exact `600` (read and write for the user only, no permissions for group or others). Your script should set this permission upon creating the file.

Example input line in `/home/user/legacy_app.log`:
`2023-10-27 15:45:00 [CRITICAL] Database connection lost`

Expected output line in `/home/user/critical_utc.log`:
`2023-10-27 06:45:00 UTC | Database connection lost`

Please write the script and run it so that the final `/home/user/critical_utc.log` file is generated and properly permissioned.
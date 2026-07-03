You are tasked with building a configuration management log processor that tracks changes across a distributed system. 

First, we have a video recording of a terminal session that encodes the history of configuration changes as embedded subtitles.
1. Extract the primary subtitle track from `/app/config_changes.mp4` to `/home/user/extracted_logs.srt`.
2. Parse the SRT file to extract just the raw log text entries (ignore the SRT sequence numbers and timing arrows). Save these clean log lines to `/home/user/extracted_logs.txt`.

Next, write a Bash script `/home/user/process_changes.sh` to process these logs.
The script must read log lines from `stdin` and write to `stdout`.
Each input log line follows this exact format:
`[YYYY-MM-DD HH:MM:SS] USER=<name> LANG=<lang> CHANGES=<N> KEY=<key_name>`
(Note: `<key_name>` may contain Unicode characters and spaces).

For every line, the script must:
- Extract the timestamp, `CHANGES` value (an integer), and `KEY`.
- Compute the rolling sum of `CHANGES` for that specific `KEY` over the last 60 minutes (3600 seconds). The window is `[current_time - 3600, current_time]` inclusive.
- The input stream is guaranteed to be chronologically sorted.
- Print the result in this exact format:
`[YYYY-MM-DD HH:MM:SS] KEY=<key_name> ROLLING_CHANGES=<sum>`

Run your script on `/home/user/extracted_logs.txt` and redirect the output to `/home/user/video_stats.txt`.

Finally, create a script `/home/user/run_processor.sh` containing the exact command:
`/bin/bash /home/user/process_changes.sh < /var/log/config.log >> /var/log/config_stats.log`
Make it executable, and schedule a cron job for the user `user` that executes `/home/user/run_processor.sh` every 5 minutes.

Your script `/home/user/process_changes.sh` will be subjected to automated equivalence testing against a reference oracle using randomly generated log streams. Ensure your Bash script is highly robust and performs the mathematical aggregations accurately.
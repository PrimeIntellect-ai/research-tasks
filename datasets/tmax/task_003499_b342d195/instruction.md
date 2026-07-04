You are a data engineer building an ETL pipeline to process multi-language telemetry logs embedded in video streams. Complete the following tasks:

1. **Log Bucketing Script**:
   Create a Python script at `/home/user/text_bucketer.py` that reads raw byte logs from standard input (`sys.stdin.buffer`). 
   - The input consists of newline-separated (`\n`) records.
   - Each record is formatted as `UNIX_TIMESTAMP|MESSAGE_BYTES`.
   - **Validation Checkpoint**: Split each line by the *first* `|` character. If a line does not contain a `|`, or if the left side cannot be parsed as a base-10 integer, silently drop the entire record.
   - **Encoding Handling**: The right side (`MESSAGE_BYTES`) may contain malformed data. Decode it as UTF-8, using the standard Unicode replacement character (`U+FFFD`) for any decoding errors.
   - **Aggregation**: For each valid record, count the number of non-ASCII characters in the decoded message (i.e., characters where `ord(char) > 127`). Bucket the counts by 1-hour intervals based on the timestamp (e.g., bucket start time = `timestamp - (timestamp % 3600)`). Sum the non-ASCII character counts per bucket.
   - **Output**: Print a single JSON object to standard output representing the aggregated data. Keys must be the bucket start times (as strings), and values must be the integer sum of non-ASCII characters. The JSON keys must be sorted in ascending order.

2. **Video Telemetry Extraction**:
   A video artefact containing embedded telemetry logs is located at `/app/telemetry.mp4`. 
   - Use `ffmpeg` to extract the raw text from the first subtitle stream (`0:s:0`) and save it to `/home/user/raw_logs.txt`. 
   - Process this extracted log file using your `text_bucketer.py` script and redirect the standard output to `/home/user/video_summary.json`.

3. **Pipeline Scheduling**:
   Configure a cron job for the current user (`user`). The cron job must execute the following exact command:
   `python3 /home/user/text_bucketer.py < /tmp/input.log > /tmp/output.json`
   Schedule this job to run every 15 minutes (e.g., `*/15 * * * *`). Ensure the cron service is active or the crontab is properly installed for the user.
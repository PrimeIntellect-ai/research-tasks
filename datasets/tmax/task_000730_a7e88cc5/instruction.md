You are tasked with organizing and extracting data from a proprietary logging system that produces high-throughput binary logs. 

There is a stripped binary located at `/app/log_generator`. When executed, it rapidly writes application logs in a custom binary format to the directory `/home/user/raw_logs/`. It constantly writes to an active file named `live.log`. Because of the high volume, the binary aggressively rotates this file: whenever `live.log` reaches exactly 512 KB, it is renamed to `archived_<timestamp>.log`, and a new `live.log` is immediately created. 

Your objective is to write a highly efficient Python script at `/home/user/extractor.py` that can run concurrently with the log generator, tail the log files, parse the custom binary format, and stream the extracted records into a single consolidated JSON Lines file at `/home/user/parsed_logs.jsonl`.

Requirements:
1. **Reverse-engineer the binary format**: Run the `/app/log_generator` for a few seconds, inspect the resulting `live.log` or archived files, and figure out the binary record structure. Every record has a fixed-size header containing a magic sequence, a timestamp, a severity level, and a payload length, followed by an ASCII message payload.
2. **Handle the rotation race condition**: Your script must use streaming I/O to read the files as they are being written. It must gracefully handle the file rotation (detecting when `live.log` is rotated away) so that no log records are dropped and no partial binary records crash your parser. 
3. **Structured Output**: Your script must parse the binary records and atomically append them to `/home/user/parsed_logs.jsonl`. 
   Each line in the JSONL file must be a valid JSON object matching this schema:
   `{"timestamp_us": <integer>, "severity": <integer>, "message": "<string>"}`
4. **Performance**: Use efficient file I/O operations (like memory mapping or buffered streaming) and keep memory usage low.

To complete the task, write your script to `/home/user/extractor.py`. We will test it by running your script in the background while running `/app/log_generator` for 30 seconds. Your script will be evaluated based on the percentage of total log records successfully captured in `parsed_logs.jsonl` without corruption.
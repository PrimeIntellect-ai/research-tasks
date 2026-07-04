I need your help organizing and archiving a set of mixed-format log files for a project. 

In the directory `/home/user/logs_raw/`, there are several log files. Some of these are plain text files ending in `.log`, and some are gzip-compressed files ending in `.log.gz`. 

I need you to create a script or run a pipeline that processes all of these log files (both compressed and uncompressed) as streams, extracts specific high-priority events, converts the format, and writes the output to a new compressed archive.

Here are the specific requirements:
1. Parse all `.log` and `.log.gz` files in `/home/user/logs_raw/`.
2. Extract only the log lines where the severity level is `[ERROR]` or `[CRITICAL]`.
3. The raw log lines have the following format:
   `YYYY-MM-DDTHH:MM:SSZ [LEVEL] The rest of the message goes here`
   Example: `2023-10-15T12:34:56Z [ERROR] Database timeout occurred`
4. Convert these extracted lines into a structured CSV format with three columns: `Timestamp`, `Level`, and `EncodedMessage`.
   - `Timestamp`: The exact timestamp string (e.g., `2023-10-15T12:34:56Z`).
   - `Level`: The severity level without the brackets (e.g., `ERROR` or `CRITICAL`).
   - `EncodedMessage`: The rest of the message (excluding the space immediately after the `]`), encoded in standard Base64.
5. Sort the resulting CSV rows chronologically by the Timestamp.
6. Write the final sorted CSV data directly to a gzip-compressed file located at `/home/user/organized_logs/critical_errors.csv.gz`. 
7. Do not include a CSV header line.
8. Ensure you do not write any intermediate uncompressed files to disk; use streaming/piping to handle the decompression, extraction, transformation, sorting, and final compression.

Please execute the necessary commands to complete this task. Let me know when you are done.
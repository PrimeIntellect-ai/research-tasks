You are a backup administrator for a high-tech manufacturing facility. Periodically, the central manufacturing server dumps a combined telemetry, log, and job-instruction stream into a highly compressed archive. You need to process the latest daily dump, extract critical error alerts for the monitoring system, and archive the proprietary manufacturing instructions (GCode) into a dedicated directory.

The dump file is located at `/home/user/robot_dump.log.gz`. 
It is a gzipped text file containing mixed data: standard log lines, critical errors, and inline multi-line GCode blocks.

Your task is to write a Python script (or use bash shell commands) to process this compressed stream *without* fully decompressing it to disk first (assume it would normally be too large for disk storage, so process it as a stream).

Perform the following operations:
1. Create a directory called `/home/user/archived_gcode/`.
2. Scan the compressed stream. Whenever you encounter a line that is exactly `[GCODE_START]`, capture all subsequent lines until you hit a line that is exactly `[GCODE_END]`. 
3. Save each captured GCode block into the `/home/user/archived_gcode/` directory. Name them sequentially as `job_1.gcode`, `job_2.gcode`, `job_3.gcode`, etc., based on the order they appear in the stream. Do not include the `[GCODE_START]` and `[GCODE_END]` tags in the output files.
4. Concurrently, identify any log lines that contain the exact string ` CRITICAL `. Extract the timestamp (which is always the first word on the line) and the rest of the message following ` CRITICAL `.
5. Save these critical logs into `/home/user/critical_errors.csv`. The format must be exactly `TIMESTAMP,MESSAGE` (e.g., if the line is `2023-10-24T10:05:00 CRITICAL Axis X limit switch hit`, the CSV line should be `2023-10-24T10:05:00,Axis X limit switch hit`).

Ensure the final `.csv` and `.gcode` files are written exactly as specified.
You are a data engineer building an ETL pipeline for a remote sensor network.

Your project manager left the exact transformation specifications and pipeline scheduling details in an audio recording located at `/app/pipeline_specs.wav`. 

Your task is to:
1. Listen to / transcribe the audio file to extract the pipeline rules.
2. Implement an executable data transformation script at `/home/user/process_data` (you can use any language, but ensure it has the correct shebang and is executable). 
3. Write the required cron schedule expression for the DAG orchestration into `/home/user/schedule.cron`.

**Data Processing Script Constraints (`/home/user/process_data`):**
- The script must read a CSV format from standard input (`stdin`).
- The input CSV will have the following columns in this exact order: `record_id`, `operator_name`, `temp_morning`, `temp_afternoon`, `temp_evening`.
- The script must reshape this wide data into a long format, mask the PII, and apply the text template EXACTLY as described in the audio recording.
- The script must write the resulting templated text lines to standard output (`stdout`), one line per long-format record. Order the output by `record_id`, and then by the period (morning, afternoon, evening).

Automated tests will invoke your script with thousands of random CSV inputs to verify its correctness against a reference implementation. Ensure your script handles arbitrary valid CSV data robustly.
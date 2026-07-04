You are acting as a log analyst investigating a flaky ETL pipeline. The pipeline has been failing and retrying, producing duplicate records. Furthermore, the log aggregator messed up character encodings, resulting in a log file with mixed UTF-8 and ISO-8859-1 (Latin-1) lines.

Your goal is to clean the logs, analyze the retry patterns, and generate a report.

1. **Character Encoding & Parsing**: 
   Read the binary log file located at `/home/user/raw_etl.log`. 
   The file contains one log entry per line. Some lines are encoded in UTF-8, while others are in ISO-8859-1.
   You must decode each line properly. If a line fails to decode as UTF-8, decode it as ISO-8859-1.
   Each decoded line has the format: `[YYYY-MM-DD HH:MM:SS] | JobID:<job_id> | <message>`

2. **Tokenization & Normalization**:
   For each log entry, normalize the `<message>` part by:
   - Converting to lowercase.
   - Removing all punctuation (replace any character that is not an alphanumeric or space with an empty string).
   - Stripping leading/trailing whitespace.

3. **Windowed Aggregation**:
   We need to identify "retry bursts". A retry burst occurs when a specific `job_id` logs the exact same normalized message **4 or more times** within any rolling **5-minute (300 seconds)** window.
   Identify all unique `job_id`s that have experienced at least one retry burst. Also, calculate the maximum number of duplicate messages within any 5-minute window for each of these bursty `job_id`s.

4. **Template-based Generation**:
   Use Python (e.g., Jinja2 or standard string formatting) to read the template file `/home/user/report_template.md` and generate a final report at `/home/user/burst_report.md`.
   The template requires a list of dictionaries containing `job_id` and `max_burst_size`, sorted in descending order of `max_burst_size`, then alphabetically by `job_id`.

**Output Requirements**:
- Save the decoded, normalized logs as a JSONL file at `/home/user/cleaned_logs.jsonl`. Each line must be a JSON object: `{"timestamp": "YYYY-MM-DD HH:MM:SS", "job_id": "...", "normalized_message": "..."}`.
- Save the final report at `/home/user/burst_report.md`.
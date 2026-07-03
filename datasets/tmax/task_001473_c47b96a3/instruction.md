You are a data scientist building a data ingestion pipeline to process and sanitize datasets before they are loaded into our machine learning platform. 

Your task is to write a Python CLI script at `/home/user/pipeline.py` that reads a JSONL (JSON Lines) input file, sanitizes and deduplicates the records, and writes the valid records to a JSONL output file. The system also runs two background services: a Redis server and an Nginx web server.

Here are the requirements for `/home/user/pipeline.py`:
1. **Invocation**: The script must accept two command-line arguments: `--input` (path to input JSONL file) and `--output` (path to output JSONL file).
   Example: `python3 /home/user/pipeline.py --input data.jsonl --output clean.jsonl`
2. **Configuration Fetch**: At the start of the script, it must download a JSON configuration file from `http://localhost:8080/config.json` (served by the local Nginx service). This config contains a `forbidden_tags` list.
3. **Record Processing**: For each line in the input JSONL file (each line is a JSON object):
   - **Character Encoding & Sanitization**: If the `description` field contains any of the tags listed in the `forbidden_tags` config (case-insensitive), or if the `description` string cannot be decoded as valid UTF-8 (i.e., contains replacement characters or encoding errors), the record must be **dropped**.
   - **Deduplication**: The script must connect to the local Redis instance (localhost:6379, db=0). It must use the `record_id` field of the record to check for duplicates. If the `record_id` already exists in a Redis Set named `seen_ids`, the record must be **dropped**. Otherwise, add the `record_id` to the Set and accept the record.
   - **Normalization**: For accepted records, strip leading and trailing whitespace from the `title` field.
4. **Output**: Write all accepted, normalized records to the file specified by `--output` in JSONL format.
5. **Template-based Reporting**: After processing a file, generate a report string exactly matching this template:
   `"Report for <input_filename>: <N> accepted, <M> dropped."`
   (e.g., `"Report for data.jsonl: 5 accepted, 2 dropped."`, using the basename of the input file). 
   Push this exact string to the end of a Redis List named `processing_reports` using the RPUSH command.

To complete the task, ensure your script handles all dependencies and connects to the running services correctly. You may use `pip` to install any necessary Python packages.
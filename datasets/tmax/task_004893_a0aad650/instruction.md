You are tasked with building an automated data-cleaning and validation pipeline for a speech-to-text machine learning project. We receive daily batches of metadata in JSON-lines format, accompanied by audio files. However, our upstream providers often send malformed data, particularly containing broken unicode escape sequences and missing timestamps. 

Your objective is to create a robust Python-based ETL pipeline that validates the JSON-lines metadata, gap-fills missing durations using the actual audio files, and is scheduled to run automatically.

Here are your specific requirements:

1. **Adversarial Validator (`/home/user/pipeline/validator.py`):**
   Write a Python script that acts as a strict filter for JSON-lines metadata.
   - It must accept a file path as an argument.
   - It must read the JSON-lines file and validate each line against these constraints:
     - The JSON must be valid (watch out for broken unicode escape sequences like `\u002` which have caused our previous parsers to crash).
     - It must contain `user_id` (integer), `transcript` (string), and `duration_sec` (float or null).
     - `duration_sec` must be strictly positive if not null.
   - If a file contains ANY invalid lines (JSON parsing errors, broken unicode, or constraint violations), the script must exit with status code `1` and print "REJECTED".
   - If all lines are valid, the script must exit with status code `0` and print "ACCEPTED".
   - We have provided a test suite of files in `/app/corpus/clean/` (which must be ACCEPTED) and `/app/corpus/evil/` (which must be REJECTED). Your script will be tested against these exact directories.

2. **Gap-Filling & Processing (`/home/user/pipeline/process.py`):**
   Write a script that takes a valid JSON-lines file and an accompanying audio file.
   - Example invocation: `python process.py metadata.jsonl /app/sample.wav output.jsonl`
   - If `duration_sec` is `null` in the JSON-lines file, your script must inspect the provided audio file (e.g., using `ffprobe` or the `wave` module) to determine the exact duration in seconds (rounded to 2 decimal places) and replace the `null` value.
   - Output the corrected JSON-lines data to the specified output file.

3. **Pipeline Scheduling:**
   - Create a bash script at `/home/user/pipeline/run_daily.sh` that runs the validator on `/home/user/incoming/data.jsonl`.
   - If accepted, it should run `process.py` using `/home/user/incoming/data.jsonl`, `/app/sample.wav`, and output to `/home/user/processed/cleaned.jsonl`.
   - Setup a cron job for the current user that executes `/home/user/pipeline/run_daily.sh` every day at 03:15 AM.

Ensure all directories (`/home/user/pipeline`, `/home/user/incoming`, `/home/user/processed`) are created. The audio fixture is located at `/app/sample.wav`.
You are an automation specialist tasked with building a robust time-series log ingestion pipeline. The system receives multi-language log entries, but the upstream source has been compromised, occasionally injecting malformed or malicious entries.

Your objective is to create a Python-based sanitization pipeline and schedule it.

**Step 1: Extract Configuration**
There is an image file located at `/app/config.png`. Use `tesseract` (pre-installed) to read this image. It contains:
1. The required exact `CRON` schedule for the pipeline.
2. A `REGEX` pattern that defines the strictly allowed payload structure for the log messages (which includes English and Japanese Unicode ranges).

**Step 2: Build the Sanitizer**
Create a Python script at `/home/user/filter.py`. 
It must be callable from the command line exactly like this:
`python3 /home/user/filter.py <input_log_file> <output_log_file>`

The script must process the input file line-by-line. Each valid line is a time-series log with the format:
`[YYYY-MM-DDTHH:MM:SS] LEVEL - PAYLOAD`

Your script must:
- Parse and validate the timestamp (must be valid ISO-8601).
- Ensure `LEVEL` is one of `INFO`, `WARN`, `ERROR`.
- Ensure the `PAYLOAD` strictly matches the `REGEX` extracted from the image.
- Drop any line that fails these checks.
- Keep all valid lines unchanged and write them to `<output_log_file>`.

**Step 3: Scheduling**
Create a bash wrapper script at `/home/user/run_pipeline.sh` that runs your Python filter on `/tmp/incoming.log` and outputs to `/tmp/processed.log`. Then, install a cron job for the `user` account that runs `/home/user/run_pipeline.sh` exactly according to the schedule extracted from the image.

Build your script carefully. The system will verify your `filter.py` against a hidden adversarial corpus of logs to ensure it perfectly drops malicious/invalid entries while preserving 100% of valid multi-language logs.
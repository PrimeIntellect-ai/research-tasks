You are a log analyst investigating a series of anomalies in a distributed computing cluster. 

The task requires you to build a robust data pipeline that extracts a decryption key from a visual transmission, safely evaluates mathematical log metrics, and joins the data with user records. 

Your final goal is to produce a Makefile and scripts that automate this entire workflow.

**Step 1: Video Artifact Processing**
You have intercepted a video file at `/app/transmission.mp4`. This video is exactly 12 seconds long at 1 frame per second (12 frames total). Each frame is either solid black or solid white.
- Extract the frames.
- Determine the binary sequence: White frames (average brightness > 128) represent `1`, Black frames (average brightness <= 128) represent `0`. Order is sequential by time.
- Convert this 12-bit binary string into a decimal integer. This is your `MULTIPLIER`.

**Step 2: Adversarial Log Filtering**
The system receives JSON logs in batches. We need a robust sanitization filter to process these logs safely.
Create a script at `/home/user/filter.py` that takes a single directory path as a command-line argument.
- The directory will contain multiple JSON files. Each file contains a JSON object with two keys: `"id"` (string) and `"metric_formula"` (string).
- The `"metric_formula"` is supposed to be a basic mathematical expression (e.g., `"(4 + 5) * 2"`, `100 / 4`).
- **However, some logs are malicious ("evil").** Attackers have injected Python code execution attempts, file-read exploits (e.g., `__import__('os')`), and severe anomalies disguised as formulas. 
- Your script must safely evaluate the mathematical expression. If it is a valid, safe mathematical expression, append the calculated numerical result as a new key `"metric_value"`.
- If the log is malicious or malformed, your script MUST completely discard it.
- Your script must print a single JSON array containing only the safely evaluated log objects to standard output (STDOUT).

**Step 3: Data Merging and DAG Orchestration**
Create a `Makefile` in `/home/user` that defines the entire pipeline DAG. The default `make` target (`all`) must:
1. Automatically extract the `MULTIPLIER` from `/app/transmission.mp4`.
2. Execute `/home/user/filter.py /app/raw_logs/` (a directory containing mixed clean and evil logs) and save the output.
3. Multiply every valid log's `"metric_value"` by the `MULTIPLIER`.
4. Join/Merge this data with the reference CSV at `/app/user_data.csv` (which has columns `id,user_name,department`) based on the `id` field.
5. Produce a final normalized, deduplicated CSV file at `/home/user/final_report.csv` with the header `id,user_name,department,final_metric`. The rows must be sorted alphanumerically by `id`.

*Note: Your `filter.py` will be independently evaluated against a hidden adversarial corpus to ensure 100% of malicious payloads are rejected and 100% of valid math expressions are preserved.*
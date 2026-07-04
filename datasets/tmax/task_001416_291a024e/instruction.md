You are a data engineer tasked with building a small, multi-language ETL pipeline to anonymize and extract features from user event logs. 

An upstream service has dumped a JSON array of events into `/home/user/input_events.json`. Each event object has the following structure:
`{"id": int, "email": string, "ip_address": string, "event_type": string, "value": int}`

Your goal is to build a two-stage pipeline orchestrated by a bash script. 

**Stage 1: Masking & Anonymization (Python)**
Create a Python script at `/home/user/mask.py` that reads `/home/user/input_events.json` and performs the following:
1. Replaces the `email` field with its SHA-256 hex digest (rename the field to `email_hash`).
2. Drops the `ip_address` field completely to protect user privacy.
3. Outputs the transformed records as a CSV file to `/home/user/masked.csv`. The CSV must have a header row with exactly these columns: `id,email_hash,event_type,value`.

**Stage 2: Feature Extraction (Node.js)**
Create a Node.js script at `/home/user/extract.js` that reads the `/home/user/masked.csv` file and performs the following:
1. Reads the CSV data.
2. Creates a new derived feature called `value_category`. If `value` is strictly greater than 50, `value_category` should be `"HIGH"`. Otherwise, it should be `"LOW"`.
3. Drops the original `value` field.
4. Outputs the final records in JSON Lines format (one JSON object per line) to `/home/user/final_features.jsonl`. 
   * Each JSON line must contain precisely these keys: `id` (as an integer), `email_hash` (string), `event_type` (string), and `value_category` (string).

**Pipeline Orchestration:**
Create an executable bash script at `/home/user/run.sh` that sequentially executes Stage 1 then Stage 2. Ensure any necessary dependencies are available or can be executed using built-in modules.

Run `/home/user/run.sh` so that the final output file `/home/user/final_features.jsonl` is successfully generated.
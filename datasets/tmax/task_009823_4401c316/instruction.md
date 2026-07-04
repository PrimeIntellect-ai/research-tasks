You are an engineer on the localization team. We receive large streams of user interaction logs from our global application, and we need to prepare this data for a new localization analytics dashboard. The raw logs contain personally identifiable information (PII) and have irregular timestamps. 

Your task is to write a Python script (`/home/user/process_logs.py`) that processes a large JSON-Lines log file (`/home/user/raw_events.jsonl`) and generates a cleaned, resampled dataset and a localized HTML report.

Here are the requirements:

1. **Large-file streaming & Anonymization**:
   - The input file `/home/user/raw_events.jsonl` is large. You must process it line-by-line (streaming) to avoid high memory usage.
   - Each line is a JSON object with keys: `timestamp`, `user_email`, `ip_address`, `event_type`, `ui_string_id`.
   - You must write the anonymized logs to `/home/user/anonymized_events.jsonl`.
   - **Anonymization rules**: 
     - `user_email`: Replace the local-part (everything before the `@`) with `***` (e.g., `alice@example.com` becomes `***@example.com`).
     - `ip_address`: Replace the last octet with `XXX` (e.g., `192.168.1.50` becomes `192.168.1.XXX`).

2. **Resampling and gap-filling**:
   - We need to know the volume of localization events per minute.
   - Extract the minute-level timestamp from each event (e.g., `2023-10-01T10:05:32Z` belongs to the minute `2023-10-01T10:05:00Z`).
   - Find the earliest and latest minute in the entire dataset.
   - Generate a CSV file at `/home/user/event_volume.csv` with columns: `minute` (in `YYYY-MM-DDTHH:MM:00Z` format) and `event_count`.
   - **Gap-filling**: Ensure EVERY minute between the earliest and latest minute (inclusive) is represented in the CSV. If a minute had no events, its `event_count` must be `0`.

3. **Template-based text generation**:
   - Create an HTML report at `/home/user/loc_report.html`.
   - The file must exactly match this template structure, filling in the bracketed variables:
     ```html
     <html>
     <body>
     <h1>Localization Operations Report</h1>
     <p>Total events processed: [TOTAL_EVENTS]</p>
     <p>Peak events in a single minute: [PEAK_COUNT]</p>
     <p>Minutes with zero events: [ZERO_MINUTES]</p>
     </body>
     </html>
     ```
   - `[TOTAL_EVENTS]` is the total number of lines in the input.
   - `[PEAK_COUNT]` is the maximum `event_count` for a single minute from your CSV.
   - `[ZERO_MINUTES]` is the number of gap-filled minutes that had 0 events.

Write and execute your Python script to produce these three files: `anonymized_events.jsonl`, `event_volume.csv`, and `loc_report.html`.
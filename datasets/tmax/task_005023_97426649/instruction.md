You are a data analyst troubleshooting a broken log export process. 

You have been provided with a CSV file at `/home/user/events.csv`. This file contains two columns: `date` (YYYY-MM-DD format) and `raw_payload`. 
The `raw_payload` is a JSON-formatted string, but the log exporter malfunctioned and wrote unicode escape sequences as literal text (e.g., it wrote `\u0045` literally as backslash, u, 0, 0, 4, 5 instead of the character `E`).

Your task is to process this file using Python and generate a gap-filled daily summary report from `2023-11-01` to `2023-11-05` (inclusive).

For each day in that date range, follow these steps:

1. **Resampling and Gap-filling**: Ensure every date in the range appears in the final report, in chronological order. 
2. **Text Normalization and Feature Extraction**: For days that have events, decode the literal unicode escape sequences in the `raw_payload` (so `\u0045` becomes `E`), parse it as JSON, and extract the string value of the `"event"` key.
3. **Similarity Computation**: For each extracted event string, calculate its similarity ratio to the target string `"SERVER_CRASH"` using Python's standard `difflib.SequenceMatcher(None, extracted_string, "SERVER_CRASH").ratio()`. Find the maximum similarity ratio among all events for that day.
4. **Template-based Generation**:
   - If the day has events, append a line to your report using exactly this template:
     `[YYYY-MM-DD] STATUS: {count} events found. Max Crash Similarity: {max_sim}`
     *(where {count} is the integer number of events that day, and {max_sim} is the maximum similarity ratio rounded to exactly 2 decimal places, e.g., 0.61).*
   - If the day has no events (a gap), append a line using exactly this template:
     `[YYYY-MM-DD] STATUS: MISSING. Max Crash Similarity: 0.00`

Save the final generated report to `/home/user/summary.txt`.

Ensure your Python script runs successfully and creates the exact formatted output required.
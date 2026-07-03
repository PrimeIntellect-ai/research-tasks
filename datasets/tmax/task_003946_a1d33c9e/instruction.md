As a localization engineer, you need to process a stream of translation telemetry logs to monitor translation velocity and quality. You have a large log file located at `/home/user/raw_translations.jsonl`. 

Write a Python script that processes this file line-by-line (to simulate large-file streaming) and performs the following tasks:

1. **Validation Checkpoint**: 
   - Only process records where `"status"` is exactly `"approved"`.
   - Only process records where `"chars"` is a positive integer (greater than 0).
   - Skip any records that do not meet these criteria.

2. **Rolling Statistics**:
   - For each valid record, calculate a rolling average of the `"chars"` translated for that specific `"lang"`, using a sliding window of the last 3 valid records (inclusive of the current record). 
   - If a language has fewer than 3 valid records so far, calculate the average using the available valid records for that language.
   - The rolling average should be a float rounded to exactly 2 decimal places.

3. **Export**:
   - Write the processed, valid records to a CSV file at `/home/user/rolling_stats.csv`.
   - The CSV must have the following header exactly: `ts,lang,chars,rolling_avg`
   - Maintain the original chronological order of the valid records.

Do not use external libraries like `pandas` (which load the entire file into memory); rely on standard Python libraries (`json`, `csv`, `collections`, etc.) to stream the file efficiently.
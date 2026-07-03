You are a data engineer tasked with fixing a legacy ETL pipeline. The current system relies on a buggy retry mechanism that frequently injects duplicate event records into the downstream data lake. 

Your objective is to write a robust Python ETL script that reads the raw text logs, extracts the required fields, normalizes them, deduplicates the "retry" records, and writes the output using a strict template format.

We have lost the original documentation for the regex patterns and deduplication rules, but a scanned snippet of the old schema specification has been recovered and is available at `/app/schema_spec.png`.

Here is your workflow:
1. **Extract Specs:** Use OCR (e.g., `tesseract`) on `/app/schema_spec.png` to recover the extraction Regex pattern and the retry deduplication time window.
2. **Process Raw Data:** Read all log files located in `/home/user/raw_data/` (e.g., `log_1.txt`, `log_2.txt`, etc.).
3. **Parse and Tokenize:** 
   - Apply the regex pattern recovered from the image to extract the Event ID, User Token, and Timestamp from each line. 
   - Note that the legacy timestamp format is idiosyncratic (Year/Day/Month). You must parse it into a standard UNIX timestamp (float) for comparison.
   - Normalize the User Token: convert to lowercase, strip all leading/trailing whitespace, and remove any non-alphanumeric characters (e.g., `@`, `-`, `$`).
4. **Deduplicate:** The retry bug causes the same User Token to fire multiple events in quick succession. If multiple records share the exact same normalized User Token AND their timestamps fall within the deduplication time window (in milliseconds) specified in the image, they are duplicates. Keep ONLY the record with the earliest timestamp. Discard the rest.
5. **Output Generation:** Write the cleaned, deduplicated records to `/home/user/clean_events.txt`. Each line must be generated using this exact template:
   `[{iso_8601_timestamp}] EVENT:{event_id} USER:{normalized_token}`
   *(Example: `[2023-12-01T15:30:00.000000] EVENT:E-9932 USER:johnsmith`)*
   Sort the final output file chronologically by timestamp.
6. **Logging:** Maintain an ETL pipeline log at `/home/user/etl.log` documenting the total lines read, total duplicates dropped, and total written.

Your final output in `/home/user/clean_events.txt` will be evaluated by an automated metrics script against a golden reference dataset. You must achieve an F1 match score of >= 0.98.
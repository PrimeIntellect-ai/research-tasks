You are a data engineer dealing with a buggy ETL pipeline. A recent bug in the data source's retry mechanism caused duplicate log entries to be injected into the data stream. Your job is to process an exported CSV of these logs, clean and deduplicate the text, calculate a rolling statistic, and generate a formatted report using Python.

The input data is located at: `/home/user/input_logs.csv`
It has three columns: `log_id`, `timestamp`, `message`. The file is already sorted by timestamp.

You must write a Python script that reads this CSV and produces a formatted text report at `/home/user/processed_logs.txt`.

Perform the following operations in order for each row:

1. **Text Normalization & Tokenization**:
   Process the `message` field using these exact rules (in order):
   - Convert the string to lowercase.
   - Normalize the string using Unicode NFKD.
   - Encode to ASCII using the 'ignore' error handler, then decode back to UTF-8.
   - Replace any character that is not a lowercase letter (a-z), a digit (0-9), or a space with an empty string (remove it).
   - Replace any sequence of multiple spaces with a single space, and strip leading/trailing whitespace.
   - The final normalized string is your "Clean Text".
   - Tokenize the "Clean Text" by splitting it on spaces. The number of resulting words is the "Token Count". (If the clean text is empty, Token Count is 0).

2. **Windowed Deduplication**:
   Due to the retry bug, duplicates appear close to each other.
   - Maintain a sliding window of the normalized "Clean Text" of the last **5** rows processed from the original stream (including those you end up dropping).
   - If the current row's "Clean Text" matches ANY of the texts in this 5-record lookback window, it is considered a duplicate.
   - **Drop** duplicates. Do not process them further, but remember they still count towards the 5-record lookback window for subsequent rows.

3. **Rolling Statistics**:
   For the records that are **kept** (not dropped), calculate a rolling average of their "Token Count".
   - The rolling average should be calculated over a window of the **3** most recent **kept** records (i.e., the current kept record and the up to 2 previous kept records).
   - Round the average to exactly 2 decimal places.

4. **Template-Based Output**:
   For every **kept** record, append a line to `/home/user/processed_logs.txt` using exactly this template format:
   `[<timestamp>] ID:<log_id> | Tokens:<count> | RollAvg:<avg_count_rounded_to_2_decimals> | Text:<normalized_text>`
   
   After all records are processed, append exactly these three lines to the end of the file:
   `=== SUMMARY ===`
   `Total Kept: <N>`
   `Total Dropped: <M>`
   (Where `<N>` and `<M>` are the respective integer counts).
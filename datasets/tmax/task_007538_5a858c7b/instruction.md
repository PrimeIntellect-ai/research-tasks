You are a Data Scientist tasked with cleaning and analyzing a messy dataset of customer service logs. 

You have been provided with a CSV file at `/home/user/raw_chat_logs.csv`. This file contains three columns: `timestamp`, `user_id`, and `message`. 

Unfortunately, the system that exported this dataset didn't properly escape text, meaning the `message` fields contain embedded newlines. Naive line-by-line processing will corrupt the records. Furthermore, the dataset contains sensitive Personally Identifiable Information (PII) and potential bot spam that needs to be detected.

Your objective is to write and execute a Python script (`/home/user/process_logs.py`) that processes this CSV using a streaming approach (row-by-row, without loading the entire file into memory at once) and performs the following operations:

1. **Robust CSV Parsing:** Read the CSV correctly, handling the embedded newlines within the `message` column.
2. **Data Masking (Anonymization):** Find any email addresses in the `message` text and replace them entirely with the exact string `[EMAIL]`. For this task, an email address is defined as any sequence of non-whitespace characters containing an `@` symbol, preceded and followed by at least one alphanumeric character (e.g., `user@example.com`, `admin-test@domain.org`).
3. **Anomaly Detection (Similarity Tracking):** We need to detect "bot-like" repetitive behavior. For each user (grouped by `user_id`), calculate the text similarity between their current message and their *immediately preceding* message (ordered chronologically by `timestamp`).
   - Use **Jaccard Similarity** on the sets of unique words in the masked messages.
   - A "word" is defined as any continuous sequence of alphanumeric characters. 
   - Convert text to lowercase before extracting words.
   - If the Jaccard Similarity between a message and the user's previous message is $\ge 0.8$, flag the current message as an anomaly (`is_anomaly = True`). Otherwise, `False`.
   - The first message from any user is never an anomaly (`False`).
4. **JSONL Output:** Write the processed records to a JSON Lines file at `/home/user/processed_logs.jsonl`. 

Each line in the output file must be a valid JSON object with the following keys:
- `timestamp` (string)
- `user_id` (string)
- `cleaned_message` (string, the masked and parsed message, retaining its original internal newlines)
- `is_anomaly` (boolean)

Write your pipeline, process the data, and ensure the output file `/home/user/processed_logs.jsonl` is perfectly formatted. You may install any necessary standard Python packages, but standard libraries like `csv`, `re`, and `json` are sufficient.
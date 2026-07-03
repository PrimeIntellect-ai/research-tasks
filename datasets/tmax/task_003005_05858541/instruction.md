You are an automation specialist tasked with creating a data processing workflow for customer service chat logs. 

We have a raw chat log file located at `/home/user/chat_logs.txt`. Each line in the file follows this format:
`[YYYY-MM-DD HH:MM:SS] <USER_ID>: <MESSAGE>`

You need to write a Python script (save it as `/home/user/process_logs.py` and run it) that performs the following tasks:

1. **Data Masking (Regex)**:
   Process each message to anonymize sensitive information.
   - Replace any email address (defined as any non-whitespace characters, followed by `@`, followed by non-whitespace characters, a dot, and non-whitespace characters, e.g., `user@domain.com`) with the exact string `[EMAIL]`.
   - Replace any US phone number in the format `XXX-XXX-XXXX` (where X is a digit) with the exact string `[PHONE]`.

2. **Feature Extraction**:
   For each message, calculate the word count. A "word" is defined as any sequence of characters separated by whitespace (use Python's default `.split()`).

3. **Aggregation**:
   Calculate summary statistics for each `USER_ID`. The statistics should include:
   - `total_messages`: The total number of messages sent by the user.
   - `average_word_count`: The average number of words per message for this user, rounded to 2 decimal places.
   - total_pii_masked: The total count of PII entities (emails + phone numbers) that were replaced for this user across all their messages.

4. **Outputs**:
   - Save the fully anonymized chat logs to `/home/user/anonymized_logs.txt`, maintaining the original format: `[YYYY-MM-DD HH:MM:SS] <USER_ID>: <ANONYMIZED_MESSAGE>`.
   - Save the aggregated statistics to `/home/user/user_stats.json`. The JSON should be a dictionary where the keys are the `USER_ID`s and the values are objects containing the calculated statistics. Format example:
     ```json
     {
       "U123": {
         "total_messages": 5,
         "average_word_count": 12.45,
         "total_pii_masked": 2
       }
     }
     ```

Ensure your script processes the file efficiently and accurately handles the regex replacements and aggregations.
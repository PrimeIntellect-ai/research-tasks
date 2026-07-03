You are a Data Scientist tasked with cleaning and anonymizing a batch of customer support transcripts before they can be used to train an NLP model. The raw data is located at `/home/user/raw_transcripts.csv`.

Your goal is to write a Python script (and any necessary setup scripts) that reads this CSV, applies specific data processing rules, and outputs a clean JSON Lines file to `/home/user/clean_transcripts.jsonl`.

Here are the strict processing requirements:

1. **Deduplication:** The dataset contains duplicate entries based on the `transcript_id`. You must keep only the *first* occurrence of each `transcript_id` (based on the order in the CSV) and discard subsequent duplicates.
2. **Date Normalization:** The `date` column contains dates in various formats (e.g., `MM/DD/YYYY`, `DD-MM-YYYY`, `YYYY/MM/DD`). Convert all dates to the standard ISO format: `YYYY-MM-DD`.
3. **Data Masking and Anonymization:** 
   - **Email:** Replace the entire value in the `customer_email` column with the literal string `[REDACTED_EMAIL]`.
   - **Credit Card:** The `cc_number` column contains 16-digit credit card numbers (sometimes with dashes, sometimes without, e.g., `1234-5678-9012-3456` or `1234567890123456`). Mask all digits except the last 4. The output must always be formatted as `XXXX-XXXX-XXXX-LAST4` (e.g., `XXXX-XXXX-XXXX-3456`).
4. **Text Normalization and Inline Redaction:** 
   - In the `transcript_text` column, convert the entire text to lowercase.
   - You must also find any email addresses embedded within the `transcript_text` (assume standard `string@string.domain` formats) and replace them with `[REDACTED_EMAIL]`.

**Output Format:**
The output must be saved to `/home/user/clean_transcripts.jsonl`. Each line must be a valid JSON object representing a row, with the exact keys:
`{"transcript_id": "...", "date": "...", "customer_email": "...", "cc_number": "...", "transcript_text": "..."}`

You can install any Python libraries you need in user-space (e.g., using `pip install --user`). Produce the final output file by the time you finish.
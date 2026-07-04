You are an automation specialist building a data ingestion pipeline for an international text aggregator. The system receives chaotic chat logs containing mixed languages, unnormalized Unicode diacritics, and irregular spacing.

Your task is to write and execute a Rust program that processes a raw data file and produces a cleaned, grouped, and enriched dataset.

**Input Data:**
A JSON Lines (JSONL) file is located at `/home/user/raw_messages.jsonl`.
Each line contains a JSON object with the following fields:
- `user_id` (string)
- `timestamp` (integer)
- `text` (string)

**Processing Requirements:**
Create a Rust project (e.g., in `/home/user/processor`) and write a tool that performs the following:

1. **Text Normalization:**
   - Apply Unicode **NFC** (Normalization Form C) to the `text`.
   - Convert the normalized text to lowercase.
   - Standardize whitespace: Replace any sequence of whitespace characters (spaces, tabs, newlines) with a single space character (` `).
   - Trim any leading or trailing whitespace from the text.

2. **Sorting & Grouping:**
   - Group the records by `user_id`.
   - Within each group, sort the records chronologically by `timestamp` (ascending). If timestamps are identical, maintain their original relative order (stable sort).
   - The final output should have the groups themselves sorted alphabetically by `user_id`.

3. **Rolling Statistics computation:**
   - For each user's chronologically sorted messages, calculate a rolling average of the message length over a sliding window of the last 3 messages (including the current one).
   - "Message length" is defined as the number of Unicode scalar values (i.e., Rust `char` count) of the *normalized* text.
   - The rolling average should be rounded to exactly two decimal places (e.g., `7.50` or `7.5`, `6.33`).

**Output Data:**
Write the processed records to `/home/user/processed_messages.jsonl` in JSON Lines format. Each line must be a JSON object containing:
- `user_id` (string)
- `timestamp` (integer)
- `normalized_text` (string)
- `rolling_avg_len` (float, rounded to 2 decimal places)

The output file must be written in the sorted order described in Step 2 (sorted by `user_id`, then by `timestamp` within each user's group).

You may use standard Rust ecosystem crates like `serde`, `serde_json`, and `unicode-normalization`.
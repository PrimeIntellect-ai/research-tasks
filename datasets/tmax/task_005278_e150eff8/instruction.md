You are a data scientist preparing a dataset for a customer support chatbot model. You have two raw datasets of customer interactions from different channels that need to be unified, cleaned, aggregated, and reshaped.

Your task is to write and execute a Python script that performs the following steps:

1. **Multi-format Reading & Schema Unification:**
   - Read `/home/user/data/chat_app.jsonl` (JSON Lines format with keys: `time`, `uid`, `msg`, `platform`).
   - Read `/home/user/data/email_support.csv` (CSV format with columns: `created_at`, `customer_id`, `content`, `origin`).
   - Unify them into a single dataset with standard columns: `timestamp` (parsed as datetime), `user_id`, `text`, and `source`.

2. **Text Normalization:**
   - Create a new column called `normalized_text`.
   - Convert `text` to lowercase.
   - Replace any character that is not an alphanumeric character (`a-z`, `0-9`) or a space with a single space.
   - Replace multiple consecutive spaces with a single space.
   - Strip leading and trailing whitespace.

3. **Windowed Aggregation:**
   - Create a new column `rolling_msg_1h`.
   - For each row, this column should contain the total number of messages sent by that specific `user_id` within the past 60 minutes up to and including the current message's `timestamp`.

4. **Wide-Long Reshaping (Summary):**
   - Create a summary dataset that counts the total number of messages per `user_id` from each source.
   - The summary dataset must be in a "wide" format with exactly three columns: `user_id`, `app` (count from chat_app), and `email` (count from email_support). Fill missing values with `0` (integer).
   - Sort this summary dataset ascending by `user_id`.

5. **Sorting & Output:**
   - Sort the main unified dataset by `user_id` ascending, then by `timestamp` ascending.
   - Save the main dataset as a Parquet file at `/home/user/output/cleaned_logs.parquet`. (Ensure `pyarrow` or `fastparquet` is installed if using pandas).
   - Save the wide-format summary dataset as a CSV at `/home/user/output/user_summary.csv` (do not include the pandas index in the CSV).

You must create the `/home/user/output/` directory if it does not exist.
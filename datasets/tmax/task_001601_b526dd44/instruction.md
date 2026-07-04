You are a data engineer tasked with building a robust ETL script to process a messy multi-language chat log CSV. The previous pipeline was silently dropping rows because user messages contained embedded newlines and multi-language Unicode characters. 

Your goal is to write a Python script at `/home/user/process_chat.py` that reads the raw data, extracts features, aggregates the time-series data, and reshapes it into a summary report.

**Input Data:**
File: `/home/user/raw_chat.csv`
Columns: `timestamp` (ISO 8601), `user_id`, `chat_room`, `message`

**Processing Requirements:**
1. **Robust Reading:** Read the CSV file correctly, ensuring that messages with embedded newlines and Unicode characters (e.g., emojis, Japanese text) are parsed accurately without dropping rows. The file uses standard CSV quoting (`"`).
2. **Feature Extraction:** Calculate a new feature `msg_len` for each row, which is the number of characters in the `message` string *after* stripping leading and trailing whitespace.
3. **Resampling and Gap-Filling:** Aggregate the `msg_len` (sum) for each `chat_room` on an hourly basis. The time range should be from the floor of the minimum timestamp to the floor of the maximum timestamp in the dataset. If a `chat_room` has no messages during a specific hour, fill the missing `msg_len` sum with `0`.
4. **Rolling Aggregation:** For each `chat_room`, compute a 3-hour rolling sum of the hourly `msg_len` (i.e., the current hour plus the two preceding hours). If there are fewer than 3 hours of history available at the start of the series, compute the sum over the available window (min_periods=1).
5. **Wide-Long Reshaping:** Pivot the dataset into a wide format where:
   - The index/rows are the hourly timestamps.
   - The columns are the distinct `chat_room` names (sorted alphabetically).
   - The values are the 3-hour rolling sum of `msg_len`.

**Output:**
Save the resulting DataFrame to `/home/user/chat_summary.csv`.
- The index must be named `timestamp` and formatted as `YYYY-MM-DD HH:00:00`.
- Missing values in the final wide format (if a room didn't exist at all until later) should be filled with `0.0`.
- The columns must be exactly the `chat_room` names.
You are a log analyst investigating application patterns. A legacy log pipeline was found to be silently dropping or corrupting log entries because it used basic `grep` and `awk` commands that break when encountering embedded newlines within CSV fields. Additionally, character encoding mismatches have caused downstream failures.

Your task is to build a robust bash script that extracts, cleans, and joins this log data correctly.

You have been provided with two input files:
1. `/home/user/raw_logs.csv`: A CSV file containing application logs. It has the columns `log_id`, `user_id`, `timestamp`, and `message`.
   - **Important:** This file is encoded in ISO-8859-1 (Latin-1).
   - The `message` column is quoted and occasionally contains embedded newlines.
   - The file may contain duplicate rows with the exact same `log_id`.
2. `/home/user/users.json`: A JSON file containing an array of user metadata objects. Each object has the fields `user_id`, `username`, and `department`.

Write a bash script at `/home/user/process_logs.sh` that performs the following steps when executed:
1. **Encoding Normalization**: Reads `raw_logs.csv` and properly converts the text to UTF-8.
2. **Deduplication**: Removes duplicate log entries based strictly on the `log_id` column (keeping only the first occurrence of each `log_id`).
3. **Newline Cleaning**: Replaces any embedded newlines *within* the CSV `message` fields with a single space character (` `). The basic CSV structure must be maintained.
4. **Data Joining**: Joins the cleaned CSV records with the user metadata from `users.json` using the `user_id` field.
5. **Formatting**: Outputs the final joined records to `/home/user/normalized_logs.jsonl` in JSON Lines (JSONL) format.

Each line in `/home/user/normalized_logs.jsonl` must be a valid JSON object containing exactly the following keys:
- `log_id` (integer or string)
- `timestamp` (string)
- `username` (string)
- `department` (string)
- `cleaned_message` (string)

**Constraints & Notes:**
- You may use any standard CLI tools available in Ubuntu (e.g., `jq`, `python3`, `iconv`, `awk`, `sed`) to construct your pipeline within the bash script.
- Do not lose any log records that contain embedded newlines.
- Ensure the script has executable permissions.
- Run your script to generate the `/home/user/normalized_logs.jsonl` file so it can be verified.
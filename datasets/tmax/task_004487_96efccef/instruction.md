You are an automation specialist setting up a data pipeline to process time-series server logs. You have been provided with two files:

1. `/home/user/logs.txt`: A raw log file containing unstructured text with timestamps.
2. `/home/user/departments.csv`: A CSV mapping user IDs to their respective departments.

Your task is to write and execute a Python script that parses the unstructured logs, extracts relevant information, joins it with the department data, anonymizes the user IDs, and outputs a structured CSV.

Requirements for the data processing:
1. **Extraction**: Parse `/home/user/logs.txt` to extract the timestamp, user ID, and error code.
   - Timestamps are formatted in brackets: `[YYYY-MM-DD HH:MM:SS]`
   - User IDs are 4-digit numbers following the word "User "
   - Error codes are alphanumeric strings starting with "ERR_" (e.g., `ERR_OOM`, `ERR_TIMEOUT`)
   - Ignore any log lines that do not contain a user ID and an error code.
2. **Masking**: Anonymize the extracted user IDs by keeping only the first two digits and replacing the rest with asterisks `*`. For example, `1234` becomes `12**`.
3. **Joining**: Match the extracted raw user ID with the `user_id` column in `/home/user/departments.csv` to find the user's department. Ignore records for which the user ID is not found in the CSV.
4. **Output**: Write the structured results to `/home/user/processed_errors.csv`.
   - The output must be a valid CSV file.
   - It must include exactly this header row: `timestamp,masked_user,dept,error_code`
   - The rows must be sorted chronologically by the timestamp.
   - `timestamp` should strictly be the `YYYY-MM-DD HH:MM:SS` portion (without brackets).

Write the necessary Python script, execute it, and ensure `/home/user/processed_errors.csv` is correctly generated.
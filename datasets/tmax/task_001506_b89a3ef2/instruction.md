You are a log analyst investigating server patterns. You need to process a messy CSV log file using only Bash and standard CLI tools (like `awk`, `sed`, `iconv`, `curl`, `grep`). Do not use Python, Perl, or other scripting languages.

Your task consists of the following steps:

1. **Local-Remote Data Transfer**: 
   A local HTTP server is hosting the raw log file. Download the file from `http://127.0.0.1:8080/raw_logs.csv` and save it to `/home/user/raw_logs.csv`.

2. **Data Cleaning and Normalization**:
   Process `/home/user/raw_logs.csv` to create a cleaned version at `/home/user/clean_logs.csv` that satisfies all of the following requirements:
   
   - **Embedded Newlines**: The `message` field (the 4th column) is enclosed in double quotes. Some messages contain embedded newlines which break standard line-by-line processing. You must replace any embedded newlines inside double quotes with a single space so that every log record occupies exactly one line.
   - **Character Encoding Handling**: The file contains some invalid UTF-8 byte sequences. Strip out any invalid UTF-8 characters (ensure the output is valid UTF-8).
   - **Constraint-Based Validation**: The `status` field (3rd column) must be one of the following HTTP status codes: `200`, `301`, `404`, or `500`. Drop any rows (excluding the header) where the status code does not match one of these valid codes.
   - **Normalization**: The `timestamp` field (2nd column) is currently in `MM/DD/YYYY HH:MM:SS` format. Convert it to ISO 8601-like `YYYY-MM-DD HH:MM:SS` format. (e.g., `12/31/2023 23:59:59` becomes `2023-12-31 23:59:59`). Leave the header row unchanged.

3. **Summary Statistics**:
   Generate a summary report of the valid HTTP status codes and save it to `/home/user/status_counts.txt`. 
   The format must be exactly:
   ```
   200: <count>
   301: <count>
   404: <count>
   500: <count>
   ```
   Only include statuses that appear in the cleaned data. Sort the output numerically by status code in ascending order.

Ensure `/home/user/clean_logs.csv` includes the CSV header row.
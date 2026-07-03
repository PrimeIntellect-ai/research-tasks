You are tasked with fixing and securing a configuration management system that tracks state changes using custom Write-Ahead Logs (WAL). 

Recently, a race condition in the system's log rotation script allowed corrupted partial writes to interleave with legitimate entries. Furthermore, an unauthorized actor has been injecting malicious configuration commands into these logs.

Your objective is to build a robust Bash-based detector that can classify a log file as either completely valid ("clean") or compromised/corrupted ("evil").

Here are your instructions:
1. **Extract Authorization Token:** 
   The system relies on a strictly enforced authorization token. The token's specification is embedded in an architecture diagram located at `/app/auth_token_schema.png`. You must use OCR (e.g., `tesseract`) to read this image and extract the correct token.

2. **Understand the Log Format:**
   A perfectly valid log file consists exclusively of lines adhering to this exact structure:
   `YYYY-MM-DD HH:MM:SS TX-NNNN <TOKEN> ACTION KEY VALUE`
   - Date/Time: Standard `YYYY-MM-DD HH:MM:SS` format.
   - Transaction ID: `TX-` followed by exactly 4 digits.
   - `<TOKEN>`: The exact authorization token extracted from the image.
   - `ACTION`: Must be one of `SET`, `UPDATE`, or `DELETE`.
   - `KEY`: Uppercase letters and underscores only (e.g., `MAX_RETRIES`).
   - `VALUE`: Alphanumeric characters and underscores only.
   *(Note: Fields are separated by exactly one space. Any trailing whitespace, missing fields, invalid actions, or mismatched tokens make the line, and thus the file, invalid).*

3. **Develop the Classifier:**
   Write a Bash script at `/home/user/wal_classifier.sh`.
   - The script must accept a single file path as its first argument: `bash /home/user/wal_classifier.sh <path_to_log>`
   - If the file is 100% valid (every single line matches the strict format and correct token), the script must exit with status code `0`.
   - If the file contains ANY invalid lines (corruptions, unauthorized tokens, wrong actions, formatting errors), the script must exit with status code `1`.
   - You are provided with training data in `/app/corpus/clean/` (all perfectly valid logs) and `/app/corpus/evil/` (logs containing various corruptions and injections). Your script must work perfectly on these.

4. **Generate a Clean Manifest:**
   Recursively traverse the `/app/corpus/clean/` directory, calculate the SHA256 checksum for every file, and output the results to `/home/user/clean_manifest.txt`. The format must exactly match the standard output of the `sha256sum` command.

Ensure your `wal_classifier.sh` script is thoroughly tested against the provided corpora, as an automated verifier will test it against a hidden holdout set of evil and clean logs.
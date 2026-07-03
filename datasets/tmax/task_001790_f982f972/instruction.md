You are a log analyst investigating suspicious activities across multiple regional servers. You need to gather logs from a simulated remote directory, normalize their formats, and extract a timeline of critical errors.

Your objective is to write and execute a Bash script that performs the following tasks:

1. **Local-Remote Transfer**: Copy all `.log` files from the simulated remote server directory at `/home/user/remote_share` to `/home/user/local_logs`. Create the local directory if it doesn't exist.

2. **Encoding Normalization**: The regional servers use different encodings:
   - `server_alpha.log` is encoded in UTF-16LE.
   - `server_beta.log` is encoded in ISO-8859-1.
   - `server_gamma.log` is encoded in UTF-8.
   Convert all files to UTF-8 in the `/home/user/local_logs` directory. You can overwrite the copied files or create new ones, as long as the final logs you process are standard UTF-8.

3. **Log Filtering (Regex & Tokenization)**: Extract only the lines that contain either `[CRITICAL]` or `[ERROR]` log levels. Extract the timestamp, the IP address, and the 3-digit numeric error code from these lines.
   The format of the log lines generally looks like this, but timestamps vary:
   `TIMESTAMP [LEVEL] IP_ADDRESS - Code ERROR_CODE: Message`

4. **Timestamp Alignment**: The servers use different timestamp formats:
   - Alpha uses Epoch timestamps (e.g., `1697025600`).
   - Beta uses US date formats (e.g., `10/11/2023 12:05:00`).
   - Gamma uses ISO-like formats (e.g., `2023-10-11 12:10:00`).
   Normalize all extracted timestamps to UTC in the strict ISO 8601 format: `YYYY-MM-DDTHH:MM:SSZ` (e.g., `2023-10-11T12:05:00Z`).

5. **Consolidation**: Save the normalized data into a CSV file located at `/home/user/suspicious_activity.csv`.
   - The CSV must have exactly this header: `Timestamp,IP_Address,Error_Code`
   - The rows must be sorted chronologically by the normalized timestamp.
   - Format example: `2023-10-11T12:00:00Z,192.168.1.10,502`

Ensure your solution relies primarily on Bash standard utilities (like `grep`, `awk`, `sed`, `iconv`, `date`, `sort`). Provide the final `/home/user/suspicious_activity.csv` file.
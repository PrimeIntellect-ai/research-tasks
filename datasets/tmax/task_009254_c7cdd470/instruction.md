As a backup administrator, you are tasked with archiving several user profile files before they are sent to off-site storage. The raw files are located in `/home/user/backups/raw/` in JSON format. Due to privacy policies, you must redact sensitive information and convert the files into a compressed, proprietary archival format.

Please complete the following steps:
1. Parse all `.json` files in `/home/user/backups/raw/`. Each file contains a JSON object with at least the keys `id`, `name`, and `email`.
2. Extract the `id`, `name`, and `email` fields.
3. Replace the actual email address of every user with the exact string `[REDACTED]`.
4. Compile the extracted and redacted data into a single CSV formatted string with the exact header `id,name,email` followed by a newline, and then one row for each user, sorted numerically by `id` in ascending order.
5. Compress this complete CSV string (including the header and all newlines) using a custom Run-Length Encoding (RLE) algorithm.
    * **Custom RLE Rules:** For the entire string, encode every consecutive sequence of identical characters as the character itself followed by the count of its consecutive occurrences. 
    * Example: The string `AABbCCC\n` must be encoded exactly as `A2B1b1C3\n1`.
6. Save the final RLE-encoded string to `/home/user/backups/archive.rle`.

You may use whatever language or tools you prefer (e.g., Python, Bash, jq) to complete this task. No external libraries are strictly required, but you can install them if you wish.
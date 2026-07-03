You are a log analyst investigating patterns in a legacy system's logs. The system produces raw logs on standard input, but they are messy, inconsistently encoded, and need to be aggregated.

We have received an image at `/app/rules.png` that contains two critical configuration parameters for the log processing pipeline:
1. The time bucket size (e.g., "15m", "1h")
2. The source character encoding of the log messages (e.g., "ISO-8859-1")

Please write a Bash script at `/home/user/process_logs.sh` that reads a stream of log lines from standard input (stdin) and processes them according to the following rules:

1. **Input Format**: Each line will start with an ISO-8601 timestamp (e.g., `2023-10-04T12:34:56Z`), followed by a single space, and then the raw log message.
2. **Filtering**: If a line does not strictly match this format (i.e., a valid ISO-8601 timestamp followed by a space and a message), ignore it entirely.
3. **Time Bucketing**: Extract the timestamp, convert it to a Unix epoch, and round it down to the nearest bucket boundary specified in `/app/rules.png`.
4. **Encoding and Cleaning**: 
   - Convert the log message from the source encoding (found in the image) to UTF-8. Drop any invalid characters during conversion.
   - Strip out all characters EXCEPT English letters (`A-Z`, `a-z`), digits (`0-9`), and spaces.
   - Convert all remaining letters to uppercase.
   - Squeeze any consecutive spaces into a single space.
5. **Output**: Print the processed line to standard output in the exact format: `BUCKETED_EPOCH|CLEANED_MESSAGE`.

Example (assuming a 10m bucket and UTF-8 source, just as an illustration):
Input: `2023-01-01T12:05:30Z System  crashed! ERROR code 0x8F`
Output: `1672574400|SYSTEM CRASHED ERROR CODE 0X8F`

Your script must handle arbitrary input lengths and random byte streams robustly without crashing. Standard tools like `iconv`, `tesseract` (for OCR), `tr`, `sed`, `awk`, and `date` are available.
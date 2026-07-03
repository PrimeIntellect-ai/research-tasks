You are a log analyst investigating patterns in a highly unusual, multilingual system log file. The system dumps metrics in a "wide" format mixed with unstructured, multi-language error messages containing complex Unicode characters. 

Your objective is to write a Rust program that parses this log file, filters the entries using a mathematical constraint, normalizes the text, and reshapes the data into a "long" format for downstream analysis.

Create a Rust project in `/home/user/log_processor` and write a program that reads `/home/user/raw_logs.txt`.

The format of `/home/user/raw_logs.txt` is:
`[{YYYY-MM-DD HH:MM:SS}] {LEVEL}: {Message} metrics:{{key1}={val1};{key2}={val2};...}`

For example:
`[2023-10-01 10:00:00] ERROR: データベース接続失敗 metrics:{alpha=3.0;beta=4.0;gamma=0.0}`

Your Rust program must perform the following tasks:
1. **Regex Pattern Construction:** Parse each line to extract the timestamp, the text message, and the key-value pairs of metrics. 
2. **Mathematical Filtering:** For each log entry, extract the numeric values of all metrics and calculate their L2 norm (Euclidean distance: the square root of the sum of the squared values). **Only keep log entries where the L2 norm is strictly greater than 5.0.**
3. **Unicode Processing:** Normalize the extracted `{Message}` text using Unicode NFKC (Normalization Form KC). This is critical because some logs contain ligatures or unnormalized characters (e.g., the ligature `ﬀ` must become `ff`). Strip any leading/trailing whitespace from the message.
4. **Wide-Long Format Reshaping:** The original log has metrics in a wide format (multiple metrics per line). You must reshape this into a long format. For every metric in a retained log entry, create a separate row.
5. **Output:** Write the results to `/home/user/processed_logs.csv` with the exact following header:
   `timestamp,metric_name,metric_value,message`

Requirements:
- Ensure the output CSV is perfectly formatted.
- You must use Rust to accomplish this. You can create the project using `cargo new /home/user/log_processor`.
- You may use external crates like `regex`, `unicode-normalization`, and `csv`.
- When your code is written, compile and run it to produce `/home/user/processed_logs.csv`.
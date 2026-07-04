You are a log analyst investigating access patterns across multiple servers. You have received a batch of log extracts in CSV format, located in `/home/user/raw_logs/`. 

Previous analysts tried to process these with simple shell pipelines, but their scripts silently dropped rows because some log messages contain embedded newlines. Furthermore, the logs come from different systems, causing mixed character encodings (some contain invalid UTF-8 bytes), and there are duplicate events recorded across different servers.

Your task is to write a Python script that robustly processes these CSV files and outputs a clean, deduplicated JSON Lines (JSONL) file.

Here are the requirements for your pipeline:

1. **Read all CSV files** in `/home/user/raw_logs/` (ending in `.csv`). The columns are: `LogID`, `Timestamp`, `User`, `RawMessage`. Note that `RawMessage` frequently contains embedded newlines.
2. **Handle Character Encodings**: Read the files handling any invalid UTF-8 characters by replacing them with the standard Unicode replacement character (U+FFFD). 
3. **Feature Extraction**: Create a new field called `Action` based on the `RawMessage`. 
   - If `RawMessage` contains the word "LOGIN" (case-insensitive), `Action` is "login".
   - Else if it contains "LOGOUT" (case-insensitive), `Action` is "logout".
   - Else if it contains "TIMEOUT" (case-insensitive), `Action` is "timeout".
   - Otherwise, `Action` is "unknown".
4. **Hash-based Deduplication**: Multiple servers often log the exact same user action. To deduplicate, compute an MD5 hash of the string formed by joining the Timestamp, User, and Action with a pipe character (i.e., `Timestamp|User|Action`). 
5. **Sorting and Filtering**: 
   - First, gather all valid rows from all CSVs.
   - Sort the combined records by `Timestamp` in ascending order. If timestamps are identical, sort by `LogID` ascending.
   - Iterate through the sorted records and keep only the *first* occurrence of each MD5 hash. Drop any subsequent records that yield the same hash.
6. **Output**: Write the deduplicated records to `/home/user/processed_logs.jsonl`. Each line must be a valid JSON object with exactly these keys, in any order:
   - `hash`: The MD5 hash string you computed.
   - `timestamp`: The original Timestamp string.
   - `user`: The original User string.
   - `action`: The extracted Action string.

Ensure your Python script is executed and successfully creates `/home/user/processed_logs.jsonl` matching the specifications exactly.
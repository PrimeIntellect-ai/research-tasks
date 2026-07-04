You are tasked with building a configuration management log processor. We have several servers that dump their configuration change logs into a central directory, but the logging systems are inconsistent. 

Write a robust Bash script at `/home/user/process_logs.sh` that reads all CSV files from `/home/user/raw_logs/`, processes them, and outputs a single aggregated and normalized CSV file at `/home/user/normalized_configs.csv`.

Here are the specific challenges and requirements you must handle:

1. **Character Encodings:** The log files are written in different encodings depending on the server OS. You must detect the encoding (e.g., using `file -i`) and convert everything to standard `UTF-8` before processing.
2. **Embedded Newlines:** The input format is CSV with a header: `ServerID,Timestamp,ConfigKey,Notes`. Some of the `Notes` fields are enclosed in double quotes and contain embedded newline characters. Standard line-by-line processing tools often silently drop or corrupt these rows. Your pipeline must correctly parse these multi-line rows.
3. **Timestamp Alignment:** The `Timestamp` column contains dates in various formats and timezones (e.g., `2023-10-25 14:30:00 PST`, `10/25/2023 10:30 PM GMT`, `2023-10-25T22:30:00Z`). You must parse and convert all timestamps into a standardized UNIX Epoch integer (seconds since 1970-01-01 00:00:00 UTC).
4. **Feature Extraction:** We do not need the full `Notes` text in the final output. Instead, replace the `Notes` column with a new feature column: `NotesLength`, representing the exact integer count of characters in the `Notes` field (excluding the enclosing quotes, but including any embedded newlines and spaces).

**Final Output Specification:**
- The script should output to `/home/user/normalized_configs.csv`.
- The output must include a header: `ServerID,EpochTimestamp,ConfigKey,NotesLength`
- The output CSV must be strictly comma-separated.
- The rows must be sorted in ascending numerical order by `EpochTimestamp`. If timestamps are identical, sort alphabetically by `ServerID`.
- You may use any standard pre-installed Linux utilities (like `bash`, `awk`, `iconv`, `date`, `python3`) inside your Bash script to accomplish this.

Ensure your script is executable (`chmod +x /home/user/process_logs.sh`) and run it so the final output file is generated.
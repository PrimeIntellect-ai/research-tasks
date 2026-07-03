I have a legacy data cleaning tool, located at `/app/legacy_cleaner`, which processes messy multilingual text logs. Unfortunately, the source code was lost, and the binary is a stripped ELF executable. I need you to write a Python script at `/home/user/cleaner.py` that exactly replicates the behavior of this binary so we can integrate it into our new Python-based ETL pipeline.

The binary takes an input CSV file and an output file path:
`/app/legacy_cleaner <input.csv> <output.csv>`

The input CSV contains three columns: `timestamp_ms`, `user_id`, and `message`. It is known to have issues like embedded newlines, corrupted or missing timestamps, and duplicate messages across multiple languages.

From my analysis, the cleaning process involves:
1. Parsing the CSV (handling embedded newlines correctly).
2. Deduplicating rows based on the SHA-256 hash of the UTF-8 encoded `message` (keeping only the first occurrence).
3. For rows with empty `timestamp_ms`, imputing the value using linear interpolation between the nearest valid preceding and succeeding timestamps.
4. Bucketing the data into 1-minute intervals based on the timestamp.

Your task is to create `/home/user/cleaner.py` such that when run as `python3 /home/user/cleaner.py <input.csv> <output.csv>`, it produces a bit-exact identical output to `/app/legacy_cleaner` for any valid input CSV. You can use the binary as a black box oracle to figure out the exact edge cases (e.g., how the first/last missing timestamps are handled, sorting, output formatting).

Good luck!
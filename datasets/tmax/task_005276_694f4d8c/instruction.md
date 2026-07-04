You are a data engineer building an ETL pipeline. A recent upstream SQL query introduced a bug involving an implicit cross join, resulting in corrupted, invalid, and mismatched records polluting our JSONL data extracts.

Your task is to write a Bash-based filter script `/home/user/etl_filter.sh` to sanitize the data. 

To know the exact business logic for what constitutes a "valid" record versus an "invalid" (cross-joined) record, you need to extract the validation rules from an image provided by the data architecture team, located at `/app/schema_rules.png`. You can use `tesseract` (which is pre-installed) to read the text from this image.

Requirements:
1. Create a script at `/home/user/etl_filter.sh`.
2. The script must read JSONL data from STDIN.
3. The script must parse each JSON object and apply the validation rules extracted from `/app/schema_rules.png`. You must implement these rules using Bash tools (like `jq`, `awk`, etc.).
4. The script must write ONLY the valid JSON records to STDOUT. Invalid records should be dropped silently.
5. The script must handle large JSONL streams efficiently.
6. Make sure the script is executable (`chmod +x /home/user/etl_filter.sh`).

The resulting script will be tested against two datasets: a clean corpus of valid records (which must be preserved exactly) and an evil corpus of invalid records (which must be completely filtered out).
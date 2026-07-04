You are an operations engineer tasked with building a configuration management auditing pipeline. You need to process raw configuration backups from multiple applications, normalize them, mask sensitive data, and fill in missing audit days (gap-filling).

You have a set of raw configuration files located in `/home/user/raw_configs/`. They are from different applications and span a specific date range, but some formats differ (INI vs JSON) and some days are missing backups.

Write a Bash script (save it anywhere, and run it) to generate a consolidated CSV report at `/home/user/config_audit.csv`.

**Requirements:**

1. **Input Parsing:**
   - Read all files in `/home/user/raw_configs/`.
   - File names follow the pattern `<app-name>_<YYYY-MM-DD>.<ext>` (e.g., `app1_2023-10-01.ini`).
   - Parse INI files (`Key=Value`) and flat JSON files (`"Key": "Value"`). Strip any whitespace, and remove quotes and commas from the JSON lines (you can assume the JSON is perfectly flat, with one key-value pair per line, excluding `{` and `}`).

2. **Normalization & Data Masking:**
   - Convert all configuration keys to lowercase.
   - If a normalized key is exactly `password` or `apikey`, replace its value with the literal string `[REDACTED]`.

3. **Gap-Filling:**
   - Identify all unique applications present in the directory.
   - The required audit period is exactly `2023-10-01` to `2023-10-05` (inclusive).
   - For every application and for every date in this 5-day period:
     - If a configuration file exists for that app and date, write its parsed, normalized, and masked key-value pairs.
     - If NO configuration file exists for that app on that date, create a single gap-fill record with the key `status` and the value `missing`.

4. **Output Format:**
   - Generate `/home/user/config_audit.csv`.
   - The first line must be the header: `date,app,key,value`
   - Every subsequent line must represent a key-value pair in CSV format: `<YYYY-MM-DD>,<app-name>,<normalized-key>,<masked-value>`
   - The data rows (excluding the header) must be sorted alphabetically by `date`, then by `app`, then by `key`.

Run your script to produce the final `/home/user/config_audit.csv` file. Do not leave the final CSV file containing any carriage returns (`\r`), standard unix line endings (`\n`) only.
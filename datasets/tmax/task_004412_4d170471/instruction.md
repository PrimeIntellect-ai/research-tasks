You are a localization engineer managing a translation pipeline. An upstream ETL job that extracts translations from our string management system experienced network timeouts and was retried multiple times. This resulted in several log files containing overlapping and duplicate translation records. Some retries simply fetched the exact same translations again, while others fetched updated translations.

Your task is to write a bash-only pipeline script at `/home/user/process_locales.sh` that extracts, deduplicates, and compiles the final translations.

The raw log files are located in `/home/user/raw_logs/`. The files are named `run1.log`, `run2.log`, etc.
They contain various application logs, but the translation entries always follow this exact pattern:
`[YYYY-MM-DDTHH:MM:SS] INFO Extracted translation -> Key: <MSG_ID> | Lang: <LANG> | Value: <TEXT>`

For example:
`[2023-10-01T12:00:00] INFO Extracted translation -> Key: LOGIN_BTN | Lang: es | Value: Iniciar sesión`

Requirements for your script:
1. **Extraction**: Parse all `.log` files in `/home/user/raw_logs/` and extract the timestamp, Key, Lang, and Value.
2. **Conflict Resolution**: If the same Key and Lang combination appears multiple times across the logs, keep only the one with the most recent timestamp. (You may assume timestamps are strictly in ISO 8601 format and safely sortable as strings).
3. **Compilation**: Write the final resolved translations to `/home/user/locales/final.csv`. The format must be a standard CSV with headers `Key,Lang,Value`. The rows must be sorted alphabetically by `Key`, and then by `Lang`.
4. **Hash-Based Duplicate Reporting**: We need to track which keys had duplicate entries across the runs. For any `Key`+`Lang` combination that appeared strictly more than once (regardless of whether the Value changed), compute the MD5 hash of the string `<Key>_<Lang>` (e.g., the MD5 of `LOGIN_BTN_es` without a trailing newline). Write these MD5 hashes to `/home/user/locales/duplicate_report.txt`, one per line, sorted alphabetically.

Ensure your script creates the `/home/user/locales/` directory if it does not exist. Run your script to generate the final output files. Only standard Linux shell tools (bash, awk, sed, grep, sort, md5sum, etc.) are allowed.
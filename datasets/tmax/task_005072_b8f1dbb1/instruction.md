You are a data analyst troubleshooting a time-series ingestion pipeline. The core component of this pipeline is a legacy compiled binary located at `/app/ts_ingester`. It processes daily CSV files containing sensor readings. 

Recently, the pipeline has been silently dropping rows or crashing. Through preliminary investigation, you suspect the binary fails catastrophically under two conditions:
1. **Embedded Newlines:** The `message` column (the 4th column) sometimes contains embedded newlines inside quotes (e.g., `"Disk full\nRebooting"`). The naive CSV parser in the binary cannot handle this and misaligns subsequent rows.
2. **Timestamp Misalignment:** The `timestamp` column (the 1st column) must be strictly in the format `YYYY-MM-DD HH:MM:SS` or `YYYY-MM-DDTHH:MM:SSZ`. Any other format (like `YYYY/MM/DD`, Unix epochs, or invalid dates) causes the binary to drop the row.

Your task is to build a classifier/gatekeeper script to protect the pipeline.
Create an executable script at `/home/user/detector.sh` that takes a single file path as its argument:
`./detector.sh <path_to_csv>`

The script must:
1. Analyze the provided CSV file.
2. Exit with status code `0` if the file is completely clean (contains NO embedded newlines anywhere, and ALL timestamps in the first column strictly match the two allowed formats).
3. Exit with status code `1` if the file contains ANY embedded newlines or ANY incorrectly formatted timestamps.
4. Append a log entry to `/home/user/pipeline.log` for every execution in the exact format:
   `[CURRENT_SYS_TIME] FILE=<basename_of_file> STATUS=<CLEAN|EVIL>`
   (e.g., `[2023-10-25 14:22:10] FILE=sensor_data.csv STATUS=EVIL`)

You can test your hypotheses about the binary's behavior by feeding it test files (`/app/ts_ingester <file>`). The binary will return exit code 139 (segfault) on embedded newlines, and print "Parse error" on bad timestamps. You must use bash, shell builtins, and standard Linux coreutils/text processing tools (awk, sed, grep, python3, etc.) to implement your detector.
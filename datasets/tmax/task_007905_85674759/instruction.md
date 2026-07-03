You are a backup administrator tasked with archiving application logs for long-term storage. You need to extract specific error events from a large, unstructured multi-line log file, enrich them with metadata, and save them into chunked CSV files.

You are provided with:
1. A multi-line log file at `/home/user/app_logs.txt`. Each log entry starts with `[START_ENTRY]` on its own line and ends with `[END_ENTRY]` on its own line. Within each entry, there are key-value pairs separated by a colon and a space (e.g., `Key: Value`). The keys present in every entry are `Timestamp`, `Level`, `ServerID`, and `Message`.
2. A JSON metadata file at `/home/user/server_metadata.json` which maps `ServerID` string codes to actual server names (e.g., `{"S1": "app-server-east", "S2": "db-server-west"}`).

Your objective is to write and execute a Python script that does the following:
1. Parses `/home/user/app_logs.txt`.
2. Filters the entries to include ONLY those where the `Level` is `ERROR` or `CRITICAL`.
3. Looks up the `ServerID` in `/home/user/server_metadata.json` and replaces it with the corresponding actual server name. If a `ServerID` is not found in the JSON file, use the string `UNKNOWN`.
4. Writes the filtered and enriched records to CSV files in the directory `/home/user/archive/`. (You must create this directory if it doesn't exist).
5. The CSV files must be chunked so that no single CSV file contains more than 50 log records.
6. The CSV files must be named sequentially as `archive_001.csv`, `archive_002.csv`, `archive_003.csv`, and so on.
7. Each CSV file must have the following header line exactly: `Timestamp,Level,ServerName,Message`
8. The values in the CSV should be properly quoted if they contain commas (standard CSV format).

Please execute your script and ensure the CSV files are created in the `/home/user/archive/` directory.
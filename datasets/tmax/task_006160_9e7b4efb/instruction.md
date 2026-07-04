I am a researcher organizing a large collection of datasets stored in various formats. I need a robust Bash script to parse metadata from these files and safely append the extracted data to a central summary file. Because I will be launching this script concurrently across hundreds of files using background jobs, it must handle file locking correctly to prevent data corruption.

Please create a Bash script at `/home/user/aggregate.sh` that does the following:

1. Takes exactly one argument: the absolute path to a dataset metadata file to process.
2. Reads my configuration file at `/home/user/config.json`. This config maps file extensions to the parsing rules needed to extract the dataset's name and its record count.
3. Parses the input file based on its extension (`.json`, `.csv`, or `.xml`). You may use `jq` for JSON, standard tools like `awk`/`cut` for CSV, and `xmlstarlet` for XML.
4. Extracts two values: the dataset name and the record count.
5. Appends a single line to `/home/user/summary.csv` in the exact format:
   `filename,dataset_name,record_count`
   (Where `filename` is just the base name of the file, e.g., `data1.json`).
6. **Critical Requirement:** You MUST use `flock` to acquire an exclusive lock on `/home/user/summary.lock` before writing to `/home/user/summary.csv` to ensure safe concurrent access.

Here is the structure of `/home/user/config.json` that you must parse to get your extraction rules:
```json
{
  "json": {
    "name_filter": ".metadata.title",
    "count_filter": ".data.total_rows"
  },
  "csv": {
    "name_column": 2,
    "count_column": 4
  },
  "xml": {
    "name_xpath": "//dataset/title",
    "count_xpath": "//dataset/records"
  }
}
```

Notes:
- For CSV files, assume they are comma-separated and have no headers.
- The script must be executable.
- Do not output anything to standard out; just safely append to the summary file.
- Assume `jq` and `xmlstarlet` are installed on the system (you can install them via `apt-get` if your script needs to ensure they are present, but run as normal user so use `sudo apt-get` if necessary, though it's best to assume they are already available).
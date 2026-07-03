You are acting as a backup administrator. Your task is to process and archive a set of multi-line application log files based on a specific configuration file.

In `/home/user/archive_rules.conf`, you will find an INI-style configuration file that specifies how to process the backups. It contains the following keys under the `[Backup]` section:
- `source_dir`: The directory containing the raw log files.
- `error_filter`: The specific log level to extract.
- `output_file`: The intermediate file where extracted data should be saved.
- `archive_name`: The final archive file path.

The log files in the `source_dir` are formatted as multi-line records separated by exactly three equals signs (`===`). Each record starts with a header line formatted as `[YYYY-MM-DD HH:MM:SS] LEVEL`, followed by one or more lines of message text.

Your objectives are:
1. Read the configuration file `/home/user/archive_rules.conf`.
2. Write a Python script (using only standard libraries) to parse all `.log` files in the specified `source_dir`.
3. Extract only the multi-line records that match the `error_filter` log level.
4. Convert the extracted records into a JSON array of objects and save it to the path specified by `output_file`. Each JSON object must have the following keys:
   - `timestamp`: The date and time string (e.g., "2023-10-01 12:00:05").
   - `level`: The log level (e.g., "CRITICAL").
   - `message`: The rest of the block's text, with lines joined by a newline character `\n` (do not include the `===` separator).
5. Finally, use standard Linux command-line tools to compress the `output_file` into a gzip-compressed tar archive (`.tar.gz`) at the path specified by `archive_name`. The archive should contain ONLY the `output_file` (with no leading directories, i.e., just the file itself in the root of the archive).

Please write and execute the necessary Python script and shell commands to complete this workflow.
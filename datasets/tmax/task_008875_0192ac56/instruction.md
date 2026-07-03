You are helping a developer organize and consolidate critical project logs scattered across a messy, deeply nested folder structure. 

The developer has a directory at `/home/user/project_logs` containing various `.log` files. 
Each log file contains application logs where a new log record always begins with a timestamp in the exact format `[YYYY-MM-DD HH:MM:SS] `. Note that a single log record might span multiple lines (e.g., a stack trace). Any line that does not start with this timestamp format is a continuation of the previous log record.

Your task is to write a Python script located at `/home/user/consolidate.py` that does the following:
1. Takes exactly two command-line arguments: the input directory (e.g., `/home/user/project_logs`) and the output file path.
2. Recursively traverses the given input directory to find all files ending in `.log`.
3. Parses the log files to extract distinct log records (handling the multi-line records correctly based on the timestamp prefix).
4. Filters the records, keeping *only* the records that contain the exact string `CRITICAL_FAILURE` anywhere in their text.
5. Writes the matching multi-line records into the output file. 
6. To prevent partial writes in case of a crash, the script **must** use an atomic write approach for the output file: write all data to a temporary file first (using the output file path appended with `.tmp`), and then atomically rename/move it to the final output file path.

**Output Formatting Requirements:**
- The records in the output file must be ordered alphabetically by the relative path of the file they were found in (relative to the input directory).
- If multiple critical records are found in the same file, they should remain in the order they appeared in that file.
- Separate each extracted record in the output file with a newline, followed by the exact string `---END_RECORD---`, followed by another newline. 

Once your script is written, execute it with `/home/user/project_logs` as the input directory and `/home/user/critical_errors.txt` as the output file.
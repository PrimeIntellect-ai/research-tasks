You are tasked with building a configuration change analyzer in C. 

A mock system root is mounted at `/home/user/sys_mount`. Inside this directory, there are various application configuration files in JSON format.
An audit system has generated a multi-line log file at `/home/user/audit.log` detailing configuration changes.

Your goal is to write a C program `/home/user/analyzer.c` that parses this log, navigates the mock file system, extracts version information from the modified JSON configuration files, and atomically writes a summary CSV file.

### Log Format
The `/home/user/audit.log` file contains multi-line records formatted as follows:
```
BEGIN RECORD
Timestamp: [unix_timestamp]
File: [absolute_path_relative_to_sys_mount]
Action: [MODIFIED | CREATED | DELETED]
Status: [SUCCESS | FAILED]
END RECORD
```

### Configuration Files
The configuration files are standard JSON files. You only need to extract the value of the `"version"` key. You can assume the version key is formatted exactly as `"version": "X.Y.Z"` (with potential varying spaces before or after the colon) on its own line or within the JSON structure. Standard C string manipulation functions (`strstr`, `sscanf`, etc.) are sufficient.

### Program Requirements
1. **Multi-line parsing:** Read `/home/user/audit.log` and identify records where `Action` is `MODIFIED` and `Status` is `SUCCESS`.
2. **Path manipulation:** For the matching records, take the `File` path (which represents an absolute path *inside* the mock mount) and resolve it to the actual file path on disk (e.g., if `File: /etc/app1/config.json`, the real path is `/home/user/sys_mount/etc/app1/config.json`).
3. **Structured parsing:** Open the resolved JSON file and extract the version string.
4. **Atomic writes:** Write the extracted data to a temporary file `/home/user/summary.csv.tmp` first. Once all records are processed and written successfully, atomically rename the temporary file to `/home/user/summary.csv`. 

### Output Format (`/home/user/summary.csv`)
The CSV file must contain a header and the matching records in the exact order they appeared in the `audit.log` file.
```csv
filepath,version
/etc/app1/config.json,1.2.4
/opt/app2/settings.json,2.0.1
```
*Note: The `filepath` in the CSV must be the original path from the log file (e.g., `/etc/app1/config.json`), not the fully resolved path.*

Write the C code, compile it using `gcc -o analyzer analyzer.c`, and run it. Do not use external JSON libraries; standard C libraries (`stdio.h`, `string.h`, `stdlib.h`, etc.) are sufficient.
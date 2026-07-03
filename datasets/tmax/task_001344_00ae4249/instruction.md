You are a backup administrator investigating a potential security incident. Recently, several users have submitted automated archive restore requests that may contain "Zip Slip" directory traversal attacks (attempting to overwrite files outside their designated restore directories).

You have a log file containing these restore requests at `/home/user/restore_requests.log`. The file uses a custom multi-line format.

Your task is to write a C program `/home/user/detect_zipslip.c` that parses this log, identifies malicious restore requests, and safely writes the findings to a CSV file.

### Log Format
The file `/home/user/restore_requests.log` contains multiple records separated by blank lines. Each record has the following format:
```
BEGIN_RECORD
ID: <alphanumeric_id>
BASE: <absolute_directory_path>
FILE: <relative_file_path_from_archive>
END_RECORD
```

### Zip Slip Detection Rules
A file path is considered malicious (a Zip Slip attempt) if it attempts to navigate above the base extraction directory. 
To determine this, process the `FILE` path component by component (separated by `/`):
1. Keep a counter representing the current directory depth, starting at `0`.
2. For each component:
   - If the component is `..`, decrement the depth by 1.
   - If the component is `.` or empty (e.g., consecutive slashes), the depth remains unchanged.
   - For any other valid directory/file name, increment the depth by 1.
3. If the depth counter drops below `0` at **any point** during the path resolution, the request is an attack.
4. If the `FILE` path starts with a `/` (absolute path), it is automatically considered an attack.

### Output Requirements
Your C program must append the identified malicious records to `/home/user/alerts.csv`. 
- The CSV format must be: `ID,FILE`
- Include a header `ID,FILE` ONLY if the file does not already exist.
- **Concurrent Access:** A background security agent is periodically reading `/home/user/alerts.csv`. Your C program **must** use exclusive file locking (e.g., `flock` or `fcntl`) on `/home/user/alerts.csv` while writing to it to prevent data corruption. 

Write the C code, compile it using `gcc`, and execute it to generate the `alerts.csv` file.
You are acting as a backup administrator archiving critical error data from an active logging system. 

There is a service that continuously writes log data to `/home/user/active_service.log`. This log file is written using `UTF-16LE` encoding. Because the service is actively writing to this file and we want to avoid reading torn or partial records, the service acquires an exclusive `flock` on the file during each write.

The log file contains multi-line records in the following format:
```
[RECORD]
TIMESTAMP: 2023-10-25T10:00:00Z
LEVEL: INFO
MSG: Backup started
DETAILS: Initiated by cron
[/RECORD]
[RECORD]
TIMESTAMP: 2023-10-25T10:01:00Z
LEVEL: ERROR
MSG: Volume shadow copy failed
DETAILS: VSS writer error 0x8004231f
[/RECORD]
```

Your task is to write and execute a script (in any language you choose) that performs the following:
1. Opens `/home/user/active_service.log` and acquires a shared lock (`flock` shared) to ensure you don't read during an active write.
2. Reads the file efficiently (e.g., streaming line-by-line or using memory-mapped I/O).
3. Parses the multi-line records and extracts **only** the records where the `LEVEL` is `ERROR`.
4. Converts the extracted data from `UTF-16LE` to `UTF-8`.
5. Outputs the extracted error records as a well-formatted JSON array of objects to `/home/user/error_archive.json`. 

The final JSON output in `/home/user/error_archive.json` must be strictly in this format:
```json
[
  {
    "TIMESTAMP": "2023-10-25T10:01:00Z",
    "LEVEL": "ERROR",
    "MSG": "Volume shadow copy failed",
    "DETAILS": "VSS writer error 0x8004231f"
  }
]
```
Ensure all keys are uppercase as they appear in the log file, and values are correctly trimmed of whitespace. Do not include the `[RECORD]` and `[/RECORD]` markers in the JSON.
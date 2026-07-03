You are tasked with automating a backup audit and reporting system. As a backup administrator, you need to verify archive integrity, parse multi-line backup logs, analyze an encoded video audit trail, and serve the consolidated results via a custom TCP server written in C++.

Perform the following steps:

1. **Archive Integrity Verification & Traversal**:
   Recursively traverse the directory `/home/user/backups/`. You will find several `.tar.gz` files. Use standard utilities to verify their integrity. Identify the exact filename of the single corrupted archive. 

2. **Multi-line Log Record Parsing**:
   Parse the log files located in `/home/user/backup_logs/`. The logs contain multi-line records formatted as follows:
   ```
   [START_BACKUP]
   ID: <backup_id>
   TIMESTAMP: <unix_timestamp>
   STATUS: <SUCCESS|FAILED>
   [END_BACKUP]
   ```
   Compile a list of `<backup_id>`s that have a `STATUS: SUCCESS`.

3. **Video Audit Trail Extraction**:
   There is a video artifact at `/app/backup_audit.mp4` representing a physical backup vault security token. 
   - Extract the frames at exactly 10 frames per second.
   - Look at the exact center pixel of each extracted frame.
   - The pixel will be either purely Black (`#000000`) or purely White (`#FFFFFF`).
   - Treat Black as `0` and White as `1`.
   - Concatenate these bits chronologically (from the first frame to the last) and decode the resulting binary sequence into ASCII characters (8 bits per character, most significant bit first). This string is your `AUDIT_TOKEN`.

4. **C++ Audit TCP Server**:
   Write a C++ program (e.g., `audit_server.cpp`) and compile it to `/home/user/audit_server`. The server must:
   - Listen for raw TCP connections on `127.0.0.1:9090`.
   - Read incoming plaintext commands ending in a newline (`\n`).
   - Respond to the following commands:
     - `GET_CORRUPTED` -> Respond with the filename of the corrupted archive (just the basename, e.g., `backup_4.tar.gz`) followed by a newline.
     - `GET_TOKEN` -> Respond with the decoded `AUDIT_TOKEN` followed by a newline.
     - `RECORD_ACCESS <text>` -> Append `<text>` to `/home/user/access.log` on a new line. Because multiple clients might send this command simultaneously, your C++ code **must** use strict POSIX file locking (`fcntl` or `flock` exclusive locks) around the file write operation to prevent race conditions. Respond with `OK\n`.
   - Run the server in the background so it is actively listening.

You may use standard Linux tools (like `ffmpeg`, `tar`, `grep`) to help solve the data parsing, but the final server must be implemented in C++. Leave the server running on port 9090 when you are done.
You are acting as a Backup Administrator. We have inherited a proprietary legacy system that continuously writes log files. Unfortunately, the service has a known race condition where log rotation interrupts the writer, leaving many log records truncated or corrupted.

Your task is to analyze the proprietary binary, process the logs it generates, and expose a network service to serve the sanitized backup.

**Step 1: Data Generation**
You have been provided with a stripped, packed legacy binary located at `/app/legacy_logger`. 
Run this binary, passing `/home/user/raw_logs` as its only argument. It will populate that directory with a recursive tree of log files.

**Step 2: C Parsing & Archiving Implementation**
Write a C program (save it as `/home/user/backup_daemon.c` and compile to `/home/user/backup_daemon`) that does the following:
1. **Recursively traverses** the `/home/user/raw_logs` directory to find all `.log` files.
2. **Parses** the multi-line records in these files. Every valid log record begins with the exact line `+-- BEGIN RECORD --+` and ends with the exact line `+-- END RECORD --+`. 
3. **Filters** the records. Due to the writer race condition, many records are missing the END marker. You must strictly ignore any record that is not properly closed by the END marker before the end of the file or before another BEGIN marker appears.
4. **Extracts** the raw contents *between* the BEGIN and END markers of all valid records and appends them sequentially into a single file at `/home/user/clean_logs.txt`.
5. **Archives** the result. The C program must programmatically (e.g., via `system()` or a library) create a gzip-compressed tarball at `/home/user/backup.tar.gz` containing the `clean_logs.txt` file at its root.

**Step 3: Network Service**
Your C program must then start a TCP server listening on `127.0.0.1:8888`.
It must accept incoming connections and handle the following protocol requests (each ending with a newline `\n`):
- `REQ: STATS\n` -> The server must reply with `COUNT=<N>\n` where `<N>` is the exact total integer count of valid records parsed across all files.
- `REQ: DOWNLOAD\n` -> The server must stream the raw binary bytes of `/home/user/backup.tar.gz` back to the client, and immediately close the connection upon finishing.

Your C program must remain running and listening for requests in the background. Do not exit.
I need you to help me organize and serve a dataset of research logs. I have a collection of raw data located in `/home/user/research_data/`.

Here is the multi-stage workflow you need to perform:

1. **Data Unpacking and Cleanup**:
   - The directory `/home/user/research_data/` contains multiple nested subdirectories, some of which contain `.tar.gz` archives. Find all `.tar.gz` archives and extract them in their respective directories.
   - You will find various `.log` files. Some of these are hard links or symlinks to other files. Delete any symlinks that are broken (point to a non-existent file).

2. **Log Processing Server (Rust)**:
   - I have a proprietary classification tool at `/app/log_scorer`. It is a compiled executable that takes a single log record via standard input and prints an integer score to standard output.
   - Write a Rust HTTP server that listens on `127.0.0.1:9090`.
   - The server must implement a `POST /process` endpoint. The request body will be a plain text string representing a directory path (e.g., `/home/user/research_data/subset_1/`).
   - When the endpoint is called, your Rust server must:
     a) Recursively traverse the requested directory.
     b) Read all valid `.log` files found.
     c) Parse the multi-line log records in each file. Records in these files are separated by a line containing exactly `---END_RECORD---`.
     d) Feed each individual multi-line record (excluding the separator) into the `/app/log_scorer` binary via stdin.
     e) Collect all records that receive a score of **75 or higher**.
     f) Respond with the concatenated high-scoring records, separated by a double newline (`\n\n`). Do not include the original `---END_RECORD---` separators.

3. **Execution**:
   - Leave the Rust server running in the background listening on port 9090.
   - Ensure you use standard Rust tools (Cargo is available).

Please be precise with the output format of the HTTP server, as my automated analysis tools will query it and expect the exact concatenated strings for the matching records.
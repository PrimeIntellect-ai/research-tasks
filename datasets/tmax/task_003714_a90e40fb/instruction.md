You are tasked with organizing and sanitizing a batch of scattered project log files. 

You have been provided with an archive of raw logs at `/home/user/incoming_logs.tar.gz`.
Your goal is to extract these logs, sanitize them concurrently using a Go program, organize them by project, and re-archive the results.

Here are the specific requirements:

1. **Extraction**: Extract `/home/user/incoming_logs.tar.gz` into the directory `/home/user/raw_logs`.

2. **Sanitization and Indexing (Go Program)**:
   Write a Go program at `/home/user/processor.go` that does the following:
   - Traverses the `/home/user/raw_logs` directory to find all `.txt` files.
   - Processes the files **concurrently** (using goroutines).
   - For each file, reads the content and redacts all standard IPv4 addresses (replace them with the exact string `[REDACTED]`).
   - Reads the first line of the file, which will always be in the format `Project: <ProjectName>` (e.g., `Project: Apollo`).
   - Saves the sanitized content to `/home/user/organized_logs/<ProjectName>/<original_filename>`. (Create directories as needed).
   - Appends a log entry to a shared index file at `/home/user/redaction_index.log` in the format: `<original_filename>,<number_of_IPs_redacted>\n`.
   - **Crucial**: Because your program processes files concurrently, you **must** use OS-level file locking (e.g., `syscall.Flock`) when writing to `/home/user/redaction_index.log` to ensure no log entries are corrupted or overwritten due to race conditions.

3. **Archiving**:
   Once the Go program finishes successfully, create a new compressed archive at `/home/user/processed_logs.tar.gz` that contains the entire `/home/user/organized_logs` directory structure.

Please write the code, execute the extraction, build and run your Go program, and create the final archive.
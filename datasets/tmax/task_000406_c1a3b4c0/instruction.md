You need to write a Go program that acts as a configuration manager tracking changes. The system generates configuration backups as `.tar.gz` archives and logs these events in a multi-line format. Your program must process these logs, verify the integrity of the archives, and securely update a global state file.

Write a Go program located at `/home/user/tracker.go`. When executed (`go run /home/user/tracker.go`), it must perform the following steps:

1. **Parse Multi-line Log Records**: Read the log file at `/home/user/backup_events.log`. The log contains multi-line records separated by double newlines (`\n\n`). Each record looks like this:
   ```
   [Event ID: <number>]
   Type: ConfigBackup
   File: <absolute_path_to_archive>
   Status: <Pending|Processed>
   ```
   Your program must extract the `File` paths for all records where the `Status` is exactly `Pending`.

2. **Verify Archive Integrity**: For each `Pending` file path extracted, verify that it is a valid, uncorrupted `.tar.gz` archive. You must do this natively in Go (e.g., using `compress/gzip` and `archive/tar`) by ensuring the gzip stream can be read and the tar headers can be parsed without errors until the EOF. If an archive is missing or corrupted, skip it.

3. **Atomic State Update with Locking**: You must update the JSON state file located at `/home/user/state.json`. To prevent race conditions with other hypothetical managers, you must acquire an exclusive file lock (using `syscall.Flock`) on the state file. 
   
   The state file initially contains: `{"valid_backups": []}`.
   
   You must read the JSON, append the absolute paths of the **valid, pending** archives to the `valid_backups` array (preserving the order they appeared in the log), and save the changes.
   
   To ensure the update is safe from crashes, you must use an atomic write pattern: write the updated JSON to a temporary file in the same directory, and then atomically rename it over `/home/user/state.json`. Finally, release the lock.

Do not use any external Go libraries; use only the standard library.
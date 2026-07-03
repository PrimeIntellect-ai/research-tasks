You are an AI assistant acting as a storage administrator. A malfunctioning log rotation script has wrecked our log directory, leaving behind fragmented log chunks, and, worse, created a recursive symlink that causes standard backup scripts to crash in an infinite loop.

Your task is to write and execute a Go program at `/home/user/resolver.go` that safely recovers the data.

The broken directory is located at `/home/user/logs`.

Your Go program must meet the following precise requirements:
1. **Traverse and Evade:** Walk through the `/home/user/logs` directory. You must explicitly ignore all symlinks to avoid falling into the infinite directory loop.
2. **Identify:** Find all regular files with the `.part` extension.
3. **Concurrent Merging:** Process the discovered `.part` files concurrently using goroutines.
4. **File Locking:** Read the text content of each `.part` file and append it to a single output file: `/home/user/logs/full_recovery.txt`. Because you are appending concurrently, your program MUST use OS-level file locking (e.g., `syscall.Flock` with `syscall.LOCK_EX`) on `full_recovery.txt` before each write to prevent data corruption. 
5. **Bulk Renaming:** Immediately after a `.part` file's contents have been safely appended to the recovery file and the lock is released, the goroutine must rename the processed file, changing its extension from `.part` to `.done` (e.g., `data.part` becomes `data.done`).

Once your program is written, compile and run it. 

Verification will check:
- The existence and line count of `/home/user/logs/full_recovery.txt`.
- That all `.part` files have been successfully renamed to `.done`.
- That the symlink loop was not followed (the program terminates successfully).
- That `syscall.Flock` was used in your source code.
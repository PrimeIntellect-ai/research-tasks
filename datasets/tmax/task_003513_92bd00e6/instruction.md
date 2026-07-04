You are acting as a backup administrator. We have an old nested archive containing server logs that need to be sanitized, merged, and chunked for a new compliance system. 

The archive is located at `/home/user/backup.tar.gz`. Inside this tarball are several `.zip` files, and inside those zip files are the raw `.log` files.

Your task is to:
1. Extract the nested archive completely.
2. Write a Go program at `/home/user/sanitize.go` that:
   - Reads all the extracted `.log` files.
   - Replaces all occurrences of the sensitive IP address `192.168.1.100` with the string `[REDACTED_IP]`.
   - Merges the sanitized contents of all log files into a single master file called `/home/user/processed/master.log`. Ensure a newline separates the contents of different files if they don't already end in one.
3. Split `/home/user/processed/master.log` into smaller chunks of exactly 50 lines each. The chunks should be named `chunk_00.log`, `chunk_01.log`, `chunk_02.log`, etc., and placed in the `/home/user/processed/` directory. (You may use standard shell tools like `split` for this final step, or do it within your Go program).

Requirements:
- Ensure the `/home/user/processed/` directory exists.
- The Go program must compile and run successfully.
- All original log data must be preserved, except for the redacted IP address.
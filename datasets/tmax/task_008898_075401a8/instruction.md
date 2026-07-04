You are an AI assistant helping a configuration manager secure its update pipeline. 

Our system receives configuration updates as compressed nested archives. Recently, we discovered that some of these updates contain "Zip Slip" vulnerabilities—archive entries with relative paths (e.g., `../../`) that attempt to overwrite files outside the intended extraction directory.

Your task is to write a Go program at `/home/user/config_extractor.go` that safely processes an incoming update bundle and logs its actions to a Write-Ahead Log (WAL).

Here are the exact specifications:

1. **Input File:** The update bundle is located at `/home/user/incoming/update.tar.gz`. Inside this archive are one or more `.zip` files.
2. **Target Directory:** All valid configuration files must be extracted to `/home/user/configs/`. You must create this directory if it doesn't exist.
3. **Zip Slip Prevention:** 
   - You must parse the nested `.zip` files and evaluate the extraction path of each file inside them.
   - If a file's resolved extraction path falls outside of `/home/user/configs/`, you MUST NOT extract it. 
   - Symbolic links inside the archives must also be evaluated. If a symlink points to a target outside `/home/user/configs/`, do not extract it.
4. **WAL Logging & File Locking:**
   - Every file evaluated in the `.zip` archives must be logged to a Write-Ahead Log at `/home/user/config.wal`.
   - Because other system processes read this WAL asynchronously, your Go program MUST acquire an exclusive file lock (using `syscall.Flock` with `syscall.LOCK_EX`) on `/home/user/config.wal` before writing each entry, and release it immediately after.
   - Append to the WAL in the following exact format for each file:
     `ENTRY: <original_zip_path> | STATUS: <EXTRACTED|SLIP_DETECTED>`
     *(Note: `<original_zip_path>` is the raw name of the file inside the zip, e.g., `app.conf` or `../../etc/passwd`)*
5. **Execution:** 
   - Compile and run your Go program so that the safe files are extracted to `/home/user/configs/` and the WAL is generated.

Ensure your code is well-structured and uses Go's standard library for archive processing and system calls.
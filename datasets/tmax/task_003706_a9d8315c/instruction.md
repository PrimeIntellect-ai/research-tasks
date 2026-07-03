You are a storage administrator managing disk space on a heavily utilized server. Users have uploaded thousands of archives to the system, but security scans indicate that some of these archives contain "Zip Slip" vulnerabilities—archive entries that attempt to extract files outside the target directory using absolute paths (e.g., `/etc/passwd`) or directory traversal sequences (e.g., `../../root/ssh`).

Your task is to write a Go program at `/home/user/audit_archives.go` that identifies these malicious archives and prepares a safe cleanup script.

Requirements for your Go program:
1. **Recursive Traversal:** Traverse the directory `/home/user/uploaded_archives/` and all of its subdirectories looking for files with `.zip` and `.tar` extensions.
2. **Archive Integrity & Inspection:** For each archive, inspect its file entries (headers) without extracting the files to disk. Flag the archive as "malicious" if any entry's file path starts with `/` or contains `../` (or `..\`). 
3. **Atomic Writes & Temp Files:** The program must write the results to `/home/user/malicious_archives.log`. To ensure no partial writes occur if the script is terminated, you must write the log to a temporary file first, and then atomically move/rename it to `/home/user/malicious_archives.log`.
    * The log file must contain the absolute path of each malicious archive, one per line, sorted alphabetically.
4. **Automated Cleanup Generation:** Atomically write a shell script to `/home/user/cleanup.sh` that, when executed, will remove all the identified malicious archives. The shell script should consist of `rm -f '<absolute_path_to_archive>'` commands, sorted alphabetically, with a standard `#!/bin/bash` shebang.
5. Run your Go program to generate `/home/user/malicious_archives.log` and `/home/user/cleanup.sh`. Do not execute the cleanup script; the automated verification will check its contents.

Ensure your Go program imports only standard library packages (`archive/zip`, `archive/tar`, `os`, `path/filepath`, `strings`, `sort`, etc.).
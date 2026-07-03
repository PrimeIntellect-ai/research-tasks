You are the site administrator for a shared local CI/CD build server. Multiple users are compiling multi-language projects (Java, C++, Python) in their respective build directories, and storage space is running out. 

Your task is to write and execute a robust Bash script that enforces a strict disk quota on these build directories by pruning the oldest build artifacts.

Specifically, you must:
1. Create a bash script at `/home/user/enforce_quota.sh`.
2. The script must iterate through all user directories located immediately under `/home/user/ci_builds/` (e.g., `/home/user/ci_builds/alice`, `/home/user/ci_builds/bob`).
3. For each user directory, check its total size in bytes (including all subdirectories and files). 
4. The maximum allowed storage (quota) per user is exactly `40000000` bytes.
5. If a user's directory exceeds this quota, the script must delete files within that user's directory tree one by one, starting from the **oldest file** (based on modification time), until the total size of the user's directory is strictly less than or equal to `40000000` bytes.
6. **Error Handling:** The script should be robust. It must ignore non-directories under `/home/user/ci_builds/`. If a file cannot be deleted, it should be skipped without halting the script, and an error logged (though for this task, you have full permissions). 
7. **Logging:** Every time a file is deleted, you must append a line to `/home/user/quota_cleanup.log` in the exact following format:
   `[CLEANUP] Deleted <full_absolute_path_to_file> recovered <file_size_in_bytes> bytes from <username>`
   *(Note: `<username>` is the name of the directory immediately under `ci_builds`, e.g., `alice`)*
8. Only delete standard files, do not delete directories.
9. After writing the script, make it executable and **run it** so that the system state is updated and the log file is generated.

Ensure your script dynamically calculates the directory size accurately during the cleanup process so it stops deleting files as soon as the directory is under quota.
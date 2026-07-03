I am organizing some old project files and need to set up a robust backup pipeline. However, I have an old proprietary indexing tool that I need to use, but it has a fatal flaw: it hangs indefinitely if it encounters cyclic symlinks (infinite symlink loops).

I need you to create a Python script located at `/home/user/clean_and_backup.py` that acts as a safe wrapper and backup orchestrator. 

Your script must take a single command-line argument, which is the path to a directory to process:
`python3 /home/user/clean_and_backup.py <target_dir>`

Here is what the script must do:
1. **Recursive Traversal & Sanitization:** Recursively traverse the provided `<target_dir>`. You must identify any cyclic symlinks (symlinks that form an infinite loop, e.g., A -> B and B -> A, or A -> A). You must **delete** these cyclic symlinks so they don't break the backup tool. Do not delete valid symlinks, even if they point outside the directory tree, as long as they resolve to a real file or directory eventually.
2. **File Processing:** For every valid, regular file found (after resolving valid symlinks), you must run our proprietary analyzer binary located at `/app/analyzer`. 
   - Usage: `/app/analyzer <absolute_path_to_file>`
   - The analyzer is a stripped binary that reads the file and outputs a single line of text (a metadata summary) to stdout. 
3. **Concurrent Logging:** Your script must take the stdout of `/app/analyzer` and append it to a log file located at `/home/user/backup_summary.txt`. Because this Python script will be triggered by multiple parallel jobs across different directories, you **must implement file locking** (e.g., using `fcntl.flock` with `LOCK_EX`) when appending to `/home/user/backup_summary.txt` to prevent race conditions and interleaved text.

To ensure your traversal and sanitization logic is bulletproof, you must carefully handle symlinks during your recursive walk. Only cyclic loops should be destroyed; safe symlinks must remain untouched. 

Please write the complete Python script at `/home/user/clean_and_backup.py`. Make sure it's executable.
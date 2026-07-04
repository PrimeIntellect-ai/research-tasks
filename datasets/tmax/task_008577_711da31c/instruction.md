You are a storage administrator tasked with investigating historical errors without exhausting the limited remaining disk space on your management server. 

You have been given a master archive file located at `/home/user/old_logs/master_archive.tar`. Because this archive was created by a legacy backup system, it is nested: it contains several inner `.tar` files (e.g., `appA.tar`, `appB.tar`), and inside those inner `.tar` files are the actual plain text `.log` files.

Your task is to extract specific error lines from these logs without extracting the archives to disk (which would waste disk space). 

Please do the following:
1. Write a Python script at `/home/user/process_logs.py` that uses the `tarfile` module to read `/home/user/old_logs/master_archive.tar`. 
2. The script must inspect the contents in memory (without writing extracted files to disk), look inside any nested `.tar` files, and read any file ending in `.log`.
3. For every line in these `.log` files that contains the exact substring `CRITICAL_FAILURE`, the script should print that line to standard output (stdout), stripping any leading/trailing whitespace.
4. Run your Python script and use shell standard stream redirection to pipe/redirect its output into the file `/home/user/critical_errors.txt`.
5. Finally, sort the contents of `/home/user/critical_errors.txt` alphabetically and save the result to `/home/user/critical_errors_sorted.txt`.

Ensure that you only output the exact matching lines, one per line. Do not print filenames or any other debugging information to standard output, as it will corrupt the output file.
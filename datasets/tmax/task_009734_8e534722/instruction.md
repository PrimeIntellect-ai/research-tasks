You are a backup administrator tasked with archiving active log files while redacting sensitive information. 

In `/home/user/active_logs/`, there is a nested directory structure containing application log files (ending in `.log`). 

Your objective is to write and execute a Go program (`/home/user/archiver.go`) that performs the following tasks:
1. Recursively traverse the `/home/user/active_logs/` directory to find all `.log` files.
2. For each `.log` file found, redact sensitive data. Specifically, you must replace:
   - Any IP address following the string "IP: " (format: `IP: X.X.X.X` where X is 1-3 digits) with `IP: REDACTED`.
   - Any Social Security Number following the string "SSN: " (format: `SSN: XXX-XX-XXXX` where X is a digit) with `SSN: ***-**-****`.
3. You must process the text transformation by orchestrating standard shell utilities (`sed`, `awk`, or `tr`) via standard stream redirection and piping within your Go code, simulating a safe backup pipeline.
4. Write the redacted logs to a new directory `/home/user/archived_logs/`, strictly preserving the original relative directory structure and file names.
5. Generate a summary log file at `/home/user/redaction_summary.txt`. For every log file processed, append a line in the exact format:
   `<relative_path_from_active_logs>: <total_number_of_redacted_lines>`
   (e.g., `app1/server.log: 4`). Sort this summary file alphabetically by the relative path before final submission.

Compile and run your Go program to perform the archival. Ensure the final redacted files exist in `/home/user/archived_logs/` and the summary file is accurately generated.

Note:
- The environment has standard Linux utilities installed.
- Do not modify the original files in `/home/user/active_logs/`.
- Ensure your Go program handles the directory creation in the target archive automatically.
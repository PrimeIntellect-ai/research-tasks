You are a support engineer investigating a pipeline failure in a log processing system. The system consists of a C program that parses CSV data files, wrapped by a shell script. Recently, the nightly jobs have been crashing. 

The application is located in `/home/user/forensics_task`. It is a Git repository. 

Your objectives are:
1. **Regression Finding:** Use `git bisect` to find the first bad commit where the script `process.sh` started failing. The tag `v1.0` is known to be good, and `HEAD` is known to be bad. Save the full commit hash of the first bad commit to `/home/user/bad_commit.txt`.
2. **Statistical Anomaly & Debugging:** The crash is caused by a segmentation fault. Use `gdb` to inspect the crash. The program reads `data.csv` which contains thousands of lines. One specific line contains a statistically anomalous sensor value that causes an out-of-bounds array access in the C code. Find the line number of this anomalous entry (1-indexed) and save it to `/home/user/anomalous_line.txt`.
3. **Environment Misconfiguration Repair:** The shell script `process.sh` sets an environment variable `DATA_DIR` which contains spaces (`/home/user/forensics_task/data files`). The C program attempts to read files from this directory using a `popen` system call, but fails to quote the directory path, leading to truncated command execution. 
4. **Fix the Code:** Modify `main.c` on the `main` branch (checkout `main` before editing) to:
   - Properly quote the directory path in the `popen` call.
   - Add a bounds check to prevent the out-of-bounds array access (ignore/skip values < 0 or >= 100).
5. **Final Output:** Compile your fixed `main.c` using `make`, then run `./process.sh`. Save the final standard output to `/home/user/final_output.txt`.

Ensure all requested output files are strictly formatted and contain exactly the requested data (e.g., just the commit hash, just the integer line number).
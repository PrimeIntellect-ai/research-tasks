I need you to help me organize some archived project files using Go and Bash. I have a nested backup archive that needs to be extracted, converted, and safely written to an output directory. 

Here are the requirements:
1. There is a nested archive located at `/home/user/organizer/backups/data.zip`. Inside this zip file is a tarball named `internal.tar.gz`. Inside that tarball are several JSON files (`log_1.json`, `log_2.json`, `log_3.json`). 
2. Use standard bash commands to extract these JSON files into `/home/user/organizer/extracted/`.
3. Write a Go program at `/home/user/organizer/process.go`. This program must:
   - Read all the extracted JSON files from `/home/user/organizer/extracted/`. Each JSON file contains an object like: `{"id": 1, "action": "commit", "user": "alice"}`.
   - Convert the extracted JSON data into a single CSV format with the header `id,action,user`.
   - Sort the CSV rows by `id` in ascending order.
   - To ensure no other process reads a partially written file, your Go program must perform an **atomic write**. Specifically, it must write the CSV output to a temporary file in `/home/user/organizer/output/`.
   - Before moving the temp file to its final destination, the program must acquire an exclusive file lock (e.g., using `syscall.Flock`) on a dedicated lock file at `/home/user/organizer/output/process.lock`.
   - Once the lock is acquired, atomically rename the temporary file to `/home/user/organizer/output/summary.csv`.
   - Finally, release the lock.
4. Run your Go program so that the final `/home/user/organizer/output/summary.csv` file is generated.

Make sure the output directory `/home/user/organizer/output/` exists before running your Go program.
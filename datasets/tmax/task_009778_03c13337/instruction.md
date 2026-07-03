You are a security researcher analyzing a suspicious dropped binary on a compromised Linux server. You have found a directory containing an executable and some database files, but the binary crashes before it completes its execution. 

Your objective is to perform forensic analysis on the binary and the abandoned data to uncover the malware's intentions.

Here are the details of the artifacts located in `/home/user/`:
- `malware_bin`: The suspicious C++ executable (compiled with debug symbols).
- `data.db` and `data.db-wal`: An SQLite database and its Write-Ahead Log. The malware seems to have crashed before committing the final transactions to the main database file.

Your tasks:
1. **System Call Tracing:** Use system tracing tools on `malware_bin` to identify the exact absolute file path it attempts to open (read) right before it crashes. The malware authors failed to handle filenames with spaces correctly, which might be related to its behavior.
2. **Interactive Debugging:** The program segfaults during execution. Use a debugger to run the program and inspect the memory at the point of the crash. Inside the `trigger_payload` function, there is a local variable containing a decryption key. Extract the value of this key.
3. **Database Recovery:** The malware left uncommitted records in the SQLite WAL file. Recover the database so that the WAL data is merged, and extract the value stored in the `info` column of the `exfiltrated_data` table.

Once you have gathered this information, create a report file at `/home/user/report.txt` with exactly three lines in the following format:
Line 1: The absolute file path the binary attempted to open before crashing.
Line 2: The decryption key extracted from memory.
Line 3: The extracted data from the database.
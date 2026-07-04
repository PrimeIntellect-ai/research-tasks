You are a storage administrator managing disk space on a Linux server. A legacy distributed application writes verbose, uncompressed log files to `/home/user/logs`. To reclaim space while preserving crucial troubleshooting data, you need to extract only the critical error records from these logs into a consolidated file, and then safely archive the original logs.

The logs contain multi-line records. A record always begins with a severity tag in brackets (e.g., `[INFO]`, `[WARN]`, `[CRITICAL]`) at the start of a line. All subsequent lines belong to that record until the next severity tag or the end of the file.

Write a C++ program at `/home/user/process_logs.cpp` and run it to do the following:
1. Iterate over all `.log` files in the `/home/user/logs` directory.
2. Parse the files to extract all multi-line records that begin with the `[CRITICAL]` tag.
3. Write these extracted `[CRITICAL]` records exactly as they appear (preserving internal line breaks) into a temporary file at `/home/user/critical_summary.tmp`.
4. Once all writing is complete, use an atomic rename operation (e.g., standard C/C++ `rename` function) to rename `/home/user/critical_summary.tmp` to `/home/user/critical_summary.txt`. This atomic write process ensures no partial files are left if the program crashes.

After running your C++ program successfully, use a shell command to bulk rename and move all the processed `.log` files from `/home/user/logs` to the directory `/home/user/archive`, changing their extensions from `.log` to `.archived` (e.g., `app1.log` becomes `/home/user/archive/app1.archived`). 

Ensure your C++ code is compiled and executed, and the final bulk rename step is completed. Do not delete the original logs; just move and rename them.
You are an AI assistant helping a technical writer organize a set of documentation drafts and logs. 

You have been provided with an archive located at `/home/user/docs.tar.gz`.

Perform the following steps:
1. **Archive Integrity & Extraction:** Verify the integrity of the gzip archive before proceeding. If it is valid, extract it into `/home/user/docs/`.
2. **Multi-line Log Parsing:** Inside the extracted directory, you will find a file named `draft_logs.txt`. It contains multi-line records separated by `---`. Use `awk`, `sed`, or other bash text-processing tools to parse this file into a single-line CSV format and save it to `/home/user/parsed_logs.csv`. The CSV should have no headers and format each record exactly as: `Author,DocName,Status`.
3. **C++ Processing with File Locking:** Write a C++ program named `/home/user/processor.cpp` that reads `/home/user/parsed_logs.csv`. For each line in the CSV, the program must:
    - Open the text file `/home/user/registry.txt` in append mode.
    - Obtain an exclusive POSIX file lock on `/home/user/registry.txt` (using `flock` or `fcntl`) to safely simulate concurrent access.
    - Write the string `[<Status>] <DocName> updated by <Author>\n` to the file.
    - Release the lock.
    - Open a binary file `/home/user/registry.bin` in append mode and write the raw binary characters of the `DocName` followed by a null byte (`\0`).
4. **Execution:** Compile the C++ program using `g++ -std=c++17 /home/user/processor.cpp -o /home/user/processor` and execute it.

Ensure that the final output files (`/home/user/parsed_logs.csv`, `/home/user/registry.txt`, and `/home/user/registry.bin`) exactly match these specifications.
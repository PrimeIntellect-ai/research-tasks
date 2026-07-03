You are tasked with building a C++ utility for an artifact manager that curates binary repositories.

We have an incoming repository with an upload log that records artifact metadata in a multi-line format. A background process is constantly appending new records to this log and uses standard file locking (`flock` with `LOCK_EX`) during writes. 

Your objective is to:
1. Fix the configuration file located at `/home/user/curator_config.ini`. It has a typo where the crucial line defining the destination directory is commented out with `# BUG: `. Use `sed` or `awk` to remove the `# BUG: ` prefix so the line reads `DESTINATION=/home/user/curated_repo`.
2. Write a C++ program at `/home/user/curator.cpp` that parses the configuration file to find the `DESTINATION` directory.
3. The C++ program must then safely read `/home/user/upload_log.txt`. Because a background process is writing to it, your C++ program **must** acquire a shared lock on the file using `flock(fd, LOCK_SH)` before reading, and release it afterward.
4. The log file contains multi-line records in the following format:
   ```
   START_ARTIFACT
   ID=<number>
   STATUS=<STABLE|UNSTABLE>
   FILE=<absolute_path>
   END_ARTIFACT
   ```
5. Your C++ program should parse this log, identify all artifacts with `STATUS=STABLE`, and write the `FILE` paths of these stable artifacts to `/home/user/stable_files.out`, with one path per line, in the order they appear in the log.
6. Compile your program to `/home/user/curator_bin` and run it.

Ensure the final output file `/home/user/stable_files.out` contains exactly the paths of the STABLE artifacts, one per line.
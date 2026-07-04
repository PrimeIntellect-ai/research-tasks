You are an artifact manager for a large Linux distribution. We have detected that threat actors are uploading malicious compiled binaries disguised within gzip-compressed artifacts.

Your task is to build a high-performance C++ artifact scanner that inspects these compressed `.gz` artifacts on-the-fly, identifies the malware, and logs the results safely.

First, you must recover the current threat intelligence. We have received an image containing the specific malware byte signature from our security team, located at `/app/security_bulletin.png`. You will need to extract the exact 23-character ASCII string labeled "BANNED_SIGNATURE:" from this image.

Second, implement the scanner in C++ (`/home/user/scanner.cpp`). The compiled binary must be located at `/home/user/scanner` and meet the following specifications:
1. **Invocation:** The program must take exactly one argument: the path to a `.gz` file. (e.g., `/home/user/scanner /path/to/artifact.gz`)
2. **Compressed Stream Processing:** The program must open the `.gz` file and read its *uncompressed* data directly in memory (e.g., using `zlib`). Do NOT extract the file to disk using shell commands or external scripts.
3. **Detection:** Search the uncompressed binary data for the exact BANNED_SIGNATURE extracted from the image.
4. **Concurrent Logging:** After determining if the file is malicious, the program must append a log entry to `/home/user/artifact_log.txt` in the format: `[FILENAME] - [CLEAN|REJECTED]\n` (e.g., `artifact1.gz - CLEAN`). Because the repository manager will invoke your scanner concurrently on many files, you **must** use POSIX file locking (`flock`) to acquire an exclusive lock on `/home/user/artifact_log.txt` before writing, and release it afterward to prevent log corruption.
5. **Exit Codes:** The program must exit with status `0` if the artifact is clean, and status `1` if the artifact is malicious (contains the signature).

We have provided a subset of historical artifacts to test against. However, your final executable will be tested against a hidden evaluation corpus using parallel execution to verify your logic, locking, and performance. 

Please construct the C++ code, compile it (ensure you link the necessary compression libraries), and verify it works against your own test cases.
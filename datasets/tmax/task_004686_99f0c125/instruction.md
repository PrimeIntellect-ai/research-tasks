As a storage administrator, you are tasked with managing disk space by extracting only the necessary critical alerts from old, compressed log archives, converting them to a structured format.

Write a C++ program at `/home/user/log_processor.cpp` that meets the following requirements:
1. **Compressed Stream Processing**: The program must take a single command-line argument representing the path to a gzipped log file (`.gz`). It must read the compressed file directly using `zlib` (do not decompress it to disk first).
2. **Multi-line Log Parsing**: The uncompressed log data is formatted in multi-line blocks like this:
   ```
   ===LOG===
   Time: 2023-10-25T08:15:30
   Status: WARNING
   Details: High memory usage detected on node 4.
   ===END===
   ```
   The program must parse these blocks and identify only the logs where `Status` is exactly `CRITICAL`.
3. **Format Conversion**: Convert the extracted CRITICAL logs into a single CSV line formatted exactly as: `Time,Status,Details` (e.g., `2023-10-25T08:15:30,CRITICAL,Node 5 crashed.`).
4. **File Locking**: Since this program might run concurrently across many archives, it must safely append the CSV lines to `/home/user/critical_events.csv`. You must use POSIX file locking (e.g., `flock(fd, LOCK_EX)`) before appending to the file and release it afterward.

To complete the task:
1. Write the C++ program at `/home/user/log_processor.cpp`.
2. Compile it to `/home/user/log_processor` (ensure you link `zlib`).
3. Execute your compiled program on both `/home/user/logs/archive1.log.gz` and `/home/user/logs/archive2.log.gz`. 

(Assume `zlib1g-dev` is installed or install it if necessary).
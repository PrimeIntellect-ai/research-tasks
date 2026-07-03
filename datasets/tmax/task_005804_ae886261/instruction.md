You have been tasked with building a safe configuration snapshot tool for a legacy system. A background process continuously updates a live binary configuration file, and occasionally rotates it. If you read the file without proper locking, you might get a corrupted read due to race conditions.

Your objective is to extract the active configuration path, write a C++ program that safely reads it using memory-mapped I/O and file locks, and then create a shell script to package the output.

**Phase 1: Configuration Extraction**
There is a manifest file located at `/home/user/manifest.conf`. It contains various settings, comments, and exactly one line specifying the active config file in the format:
`ACTIVE_CONFIG_PATH = /home/user/live_config.bin` (there may be varying whitespace).
Use text transformation tools (like `sed` or `awk`) to extract just the file path and save it to `/home/user/active_path.txt`.

**Phase 2: Safe Reader (C++)**
Write a C++ program at `/home/user/safe_reader.cpp` and compile it to `/home/user/safe_reader`. 
The program must:
1. Accept exactly one command-line argument: the path to the file to read.
2. Open the file and acquire a shared (read) POSIX file lock using `fcntl` (F_SETLKW) to wait for any exclusive writers to finish.
3. Once locked, use `mmap` to map the entire file into memory.
4. Write the entire mapped memory to `stdout` (using streaming or standard I/O).
5. Unmap the memory, release the lock, and close the file.

**Phase 3: Backup Script**
Write a bash script at `/home/user/package_backup.sh` that does the following:
1. Reads the target file path from `/home/user/active_path.txt`.
2. Executes `/home/user/safe_reader` with that path.
3. Compresses the output of the reader directly into a gzip file named `/home/user/snapshot.gz`.
4. Packages the `snapshot.gz` file into an uncompressed tar archive named `/home/user/snapshot.tar`. (This is a nested archive: a gzip inside a tar).
5. Creates a symbolic link at `/home/user/latest_backup.link` pointing to `/home/user/snapshot.tar`.

Ensure your C++ code handles errors gracefully (e.g., if the file cannot be opened). Do not run the backup script continuously, just ensure the scripts and binaries are correctly created and functional.
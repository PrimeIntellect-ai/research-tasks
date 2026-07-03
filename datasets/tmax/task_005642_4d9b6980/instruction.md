You are acting as a storage administrator who needs to optimize disk space on a log server. The server generates highly repetitive, uncompressed CSV log files. Your task is to write a C++ program that securely converts these CSV files into a tightly packed, zlib-compressed binary format while handling concurrent access safeguards. 

The logs are located in `/home/user/logs/`. There are multiple `.csv` files.

Your C++ program must do the following:
1. Scan the `/home/user/logs/` directory for all files ending in `.csv`.
2. For each CSV file, open it and immediately attempt to acquire an exclusive file lock using `flock(fd, LOCK_EX)`. This is required because a background service occasionally writes to these files. If the file is locked, your program must wait until the lock is released.
3. Once locked, parse the CSV. The CSV has no header. Each line is formatted as: `timestamp,user_id,action_code,payload_size`
   - `timestamp` fits in a standard unsigned 64-bit integer (`uint64_t`).
   - `user_id` fits in an unsigned 32-bit integer (`uint32_t`).
   - `action_code` fits in an unsigned 16-bit integer (`uint16_t`).
   - `payload_size` fits in an unsigned 32-bit integer (`uint32_t`).
4. Convert the parsed data into a continuous sequence of binary structs (packed, without padding). The struct must exactly match the byte order of the fields listed above (14 bytes total per record).
5. Compress the binary data using zlib (`gzopen`, `gzwrite`, etc.) and write it to a new file in the same directory named `<original_filename_without_extension>.bin.gz`.
6. Release the lock.
7. Once a file is successfully converted and the compressed file is closed, rename the original CSV file by appending `.bak` to its name (e.g., `server1.csv` becomes `server1.csv.bak`). This serves as our bulk renaming step for archived files.

Requirements & Constraints:
- Use C++ for the core logic. You may write bash scripts to compile and run your code.
- You will need to install any necessary C++ development libraries (e.g., `zlib1g-dev`) using `sudo apt-get`. (You have passwordless sudo access).
- You must compile your C++ code to an executable named `/home/user/log_converter`.
- Create a text file `/home/user/completion.txt` containing the word "DONE" when the process has fully completed.

Ensure your parsing is robust to standard newline characters. We will verify your task by running a script that decompresses the `.bin.gz` files and checks the binary structs against the original data, and verifies the locks were properly utilized.
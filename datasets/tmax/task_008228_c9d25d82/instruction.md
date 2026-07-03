I am a researcher dealing with a continuous stream of experimental data files. Sometimes, the experimental sensors output duplicate data (different filenames, but identical content). I need a C program that acts as a background watcher to automate incremental archiving of this data while avoiding duplicates.

Please write a C program that fulfills these requirements:

1. **Directories & Files:**
   - Watch Directory: `/home/user/incoming`
   - Archive File: `/home/user/backup/master.tar`
   - Log File: `/home/user/backup/watcher.log`
   - Source File: `/home/user/src/watcher.c`
   - Executable: `/home/user/bin/watcher`

2. **Functionality:**
   - Use Linux `inotify` to monitor the `/home/user/incoming` directory.
   - Listen specifically for files that are closed after being written (`IN_CLOSE_WRITE`).
   - Only process files with a `.dat` extension. Ignore all other files.
   - When a `.dat` file is detected:
     a. Compute the SHA256 hash of the file's contents. You may use `openssl/sha.h` or any standard library.
     b. Check if a file with this exact SHA256 hash has already been archived. (You can maintain this state in memory, or by reading the log file).
     c. **If it's new data:** Append the file to the uncompressed tar archive `/home/user/backup/master.tar`. You can invoke the system `tar` command to append (`tar -rf ...`). Then append a line to the log file in the exact format: `ADDED <filename> <sha256>`
     d. **If it's duplicate data (hash already seen):** Do NOT add it to the archive. Delete the file from `/home/user/incoming`. Append a line to the log file in the exact format: `DUPLICATE <filename> <sha256>`
   - The program should run continuously until it receives a `SIGINT` (Ctrl+C), at which point it should exit cleanly (flush files, close handles).

3. **Execution:**
   - Write the code in `/home/user/src/watcher.c`.
   - Compile it to `/home/user/bin/watcher`. Make sure to link `libcrypto` if using OpenSSL (`-lcrypto`).
   - You do NOT need to run the watcher permanently. Once you have compiled it and verified it works with a few test files, you have completed the task. Ensure all paths exist before you finish.

Please create the necessary directories, write the C code, compile it, and leave the executable ready at `/home/user/bin/watcher`.
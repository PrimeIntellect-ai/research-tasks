You are a storage administrator working to automate disk space management on a Linux server. We need a custom C daemon that monitors a "hot data" ingest directory and automatically archives files into a "cold storage" directory once they are fully written, verifying the archive integrity before deleting the original file to save space.

Your task is to implement this workflow by writing a C program, compiling it, and processing a set of test files.

Follow these instructions exactly:

1. **Setup:**
   - Create the watch directory: `/home/user/hot_data`
   - Create the archive directory: `/home/user/cold_archive`
   - Create a log file: `/home/user/audit.log`

2. **Write the C Program:**
   - Write a C program at `/home/user/archiver.c`.
   - The program must take exactly two command-line arguments: the watch directory and the archive directory. Example: `./archiver /home/user/hot_data /home/user/cold_archive`
   - It must use Linux `inotify` to monitor the watch directory for the `IN_CLOSE_WRITE` event (which indicates a file was opened for writing and has just been closed).
   - Whenever an `IN_CLOSE_WRITE` event occurs for a file (e.g., `data.txt`), the program must:
     a) Create a compressed tar archive of the file in the archive directory. The archive name must be `<filename>.tar.gz`. You can invoke the system `tar` command via `system()` or `fork()/exec()`. For example: `tar -czf /home/user/cold_archive/data.txt.tar.gz -C /home/user/hot_data data.txt`.
     b) Verify the archive's integrity by testing it (e.g., using `tar -tzf <archive_path>`).
     c) If the verification succeeds, delete the original file from `/home/user/hot_data` using `unlink()`.
     d) Finally, append a log entry to `/home/user/audit.log` in this exact format:
        `ARCHIVED AND VERIFIED: <filename>\n` (e.g., `ARCHIVED AND VERIFIED: data.txt`).
   - The program should run in an infinite loop listening for events. Ensure you handle standard C includes and compile it cleanly.

3. **Compile and Run:**
   - Compile the program to an executable named `/home/user/archiver`. Standard `gcc` is available. 
   - Start the program in the background watching `/home/user/hot_data` and outputting to `/home/user/cold_archive`.

4. **Trigger the Archiving (Testing):**
   - While your archiver is running in the background, create the following three files in `/home/user/hot_data` sequentially (allow a second between each to ensure the archiver processes them):
     - `report.csv` containing the text: `id,value\n1,100`
     - `image.bin` containing exactly 1024 bytes of `/dev/urandom` data.
     - `system.log` containing the text: `[WARN] Disk space running low`
   
5. **Final Validation:**
   - Ensure the original files are no longer in `/home/user/hot_data`.
   - Ensure `/home/user/cold_archive` contains `report.csv.tar.gz`, `image.bin.tar.gz`, and `system.log.tar.gz`.
   - Ensure `/home/user/audit.log` contains the three confirmation lines. Leave the background process running.
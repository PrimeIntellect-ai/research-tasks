You are a storage administrator managing a legacy file drop system. Old systems periodically dump log files into a specific directory. These files have messy names (containing spaces and mixed casing) and are encoded in legacy `Windows-1252`. You need to clean these up to reclaim disk space and standardize the data for modern log ingest tools, which require `UTF-8` and strict naming conventions.

Your task is to build and test an automated storage management workflow using Python.

Phase 1: Dependency and Directory Setup
1. Create two directories: `/home/user/storage_drop` (where legacy files arrive) and `/home/user/storage_archive` (where processed files are stored).
2. Install any necessary Python packages to monitor file system events (e.g., `watchdog`).

Phase 2: The Storage Manager Script
Write a Python script at `/home/user/storage_manager.py` that does the following:
1. Takes two directory paths as arguments (input and output).
2. Upon starting, immediately processes all existing files in the input directory.
3. Begins continuously monitoring the input directory for any newly created files, processing them immediately as they arrive.
4. **Processing rules:**
   - **Encoding Conversion:** Read the input file using `Windows-1252` encoding and write the contents to the output directory using `UTF-8` encoding.
   - **Bulk Renaming:** The output filename must be derived from the input filename by converting all characters to lowercase, replacing all spaces with underscores, and appending `.processed` to the end. (For example, `Server Log 1.txt` becomes `server_log_1.txt.processed`).
   - **Cleanup:** Delete the original file from the input directory after processing.

Phase 3: Execution and Verification
To prove your system works:
1. Manually create a file named `Legacy Dump.txt` inside `/home/user/storage_drop` containing the text `Voilà, testing storage` encoded in `Windows-1252`.
2. Run your `storage_manager.py` script in the background, pointing it to watch `/home/user/storage_drop` and output to `/home/user/storage_archive`.
3. Wait 2 seconds, then simulate a new incoming file by creating `/home/user/storage_drop/New Server Events.log` containing the text `Café server crashed` encoded in `Windows-1252`.
4. Give the script a moment to process the new file.
5. Use standard stream redirection to output the directory listing of `/home/user/storage_archive` into `/home/user/final_state.log` (e.g., `ls -1 /home/user/storage_archive > /home/user/final_state.log`).
6. Terminate your background Python script.

Ensure all file paths, encodings, and renaming rules are strictly followed.
You are an AI assistant helping a storage administrator manage disk space by archiving critical error logs. 

We have a directory of log files at `/home/user/logs/`. You need to write and execute a C++ program that consolidates these logs into a single archive based on a configuration file, then safely marks the original files as processed.

Your C++ program must be saved at `/home/user/archiver.cpp` and should do the following:
1. **Configuration file interpretation**: Read the configuration file located at `/home/user/config.txt`. It contains two lines in `KEY=VALUE` format:
   - `ARCHIVE_PATH`: The absolute path where the final archive should be saved.
   - `FILTER_KEY`: The keyword to filter log lines by.

2. **Streaming I/O**: Iterate through all `.log` files in `/home/user/logs/` in alphabetical order. Read each file line by line to minimize memory usage. Extract only the lines that contain the `FILTER_KEY` (case-sensitive).

3. **Format conversion**: Combine the extracted lines into a simple custom archive format. For each file that contains at least one matching line, write a header `=== <filename> ===\n` (where `<filename>` is just the base name of the file, e.g., `app.log`), followed by the matching lines exactly as they appeared. Do not write a header if the file has no matching lines.

4. **Atomic writes**: Write the archived output to a temporary file first (e.g., appending `.tmp` to the target path). Once all processing is complete and the file is fully written, atomically rename the temporary file to the final `ARCHIVE_PATH` specified in the config.

5. **Bulk file renaming**: After successfully creating the archive, rename all processed `.log` files in the `/home/user/logs/` directory to have a `.log.processed` extension.

Compile your C++ program using `g++ -std=c++17` and run it to process the logs. 

Ensure the final system state has the successfully created archive file at the expected location and the old log files renamed.
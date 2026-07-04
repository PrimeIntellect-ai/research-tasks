You are an AI assistant helping a developer organize and transform incoming telemetry logs for a project. 

The system receives raw telemetry data in a specific directory. Some of this data is plain text, and some is gzip-compressed. Your goal is to build a C++ application that parses these logs and a Bash script that acts as a simple file watcher to process incoming files dynamically.

Here are the requirements:

1. **Directories**:
   Assume the following directories exist (you should create them if they don't):
   - `/home/user/incoming` (where new logs arrive)
   - `/home/user/processed` (where your C++ program will write the extracted data)
   - `/home/user/archive` (where the Bash script will move files after processing)

2. **The C++ Log Filter (`/home/user/filter.cpp`)**:
   Write a C++ program that takes a single command-line argument: the absolute path to an input log file.
   - The program must handle both plain text files (e.g., ending in `.log`) and gzip-compressed files (ending in `.gz`).
   - For `.gz` files, your C++ program must use `popen` to decompress the stream on the fly using standard bash utilities (e.g., `zcat` or `gunzip -c`), rather than relying on external C++ compression libraries. For `.log` files, read them directly using standard file streams.
   - The log lines have the exact format: `TIMESTAMP | MODULE | LEVEL | MESSAGE`
   - Example line: `2023-10-01 12:00:00 | Network | FATAL | Connection timeout`
   - Your program must parse the file line by line, look for lines where `LEVEL` is exactly `FATAL`, and append the raw, unmodified line to a file named `/home/user/processed/<MODULE>.log`. 
   - Note: `<MODULE>` should be extracted from the line (trimming any surrounding whitespace).

3. **The Bash File Watcher (`/home/user/watch.sh`)**:
   Write a Bash script that continuously monitors the `/home/user/incoming` directory for new files.
   - When a file ending in `.log` or `.gz` appears, the script should invoke your compiled C++ program (which you should compile to `/home/user/filter`) on that file.
   - After the C++ program finishes processing the file, the Bash script must move the file to `/home/user/archive/`.
   - If a file named `EOF.txt` appears in `/home/user/incoming`, the script should exit gracefully with code `0`.

4. **Execution**:
   Once you have written and compiled `/home/user/filter.cpp` to `/home/user/filter`, and written `/home/user/watch.sh`, make sure `watch.sh` is executable. You do not need to run `watch.sh` in the background; you can run it directly in your terminal. There is a background process that will drop files into the `incoming` directory shortly after you start the script, eventually dropping `EOF.txt`.

Write the code, compile it, and run your watcher script to process the test data.
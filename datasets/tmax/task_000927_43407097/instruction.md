You are a backup administrator responsible for archiving critical system logs. We have an old proprietary archiving tool, but the source code is lost. You only have the compiled, stripped executable located at `/app/arc_tool`. 

Your goal is to build a TCP service in Bash that dynamically parses logs, extracts specific records, compresses them using the provided binary, and serves the result to requesting clients.

Here are the requirements:

1. **Log Parsing:**
   The raw logs are located in `/home/user/logs/` and are named `app_<YYYY-MM-DD>.log`. The logs consist of multi-line records. Each record begins with `--- RECORD START ---`, contains multiple lines of key-value pairs (including `DATE: YYYY-MM-DD` and `LEVEL: <INFO|WARNING|CRITICAL>`), and ends with `--- RECORD END ---`. 
   You must extract ONLY the records where `LEVEL: CRITICAL`.

2. **Custom Compression (The Oracle):**
   The binary at `/app/arc_tool` takes two arguments: an input file and an output file. It reads the input file and writes a custom compressed format to the output file. 
   Usage: `/app/arc_tool <input.txt> <output.arc>`

3. **Concurrency and Locking:**
   Your service must handle multiple concurrent requests. Since the extraction and compression process writes to temporary working directories, you must use standard Linux file locking (`flock`) on a lockfile located at `/tmp/archive.lock` to ensure that concurrent requests do not corrupt each other's temporary files.

4. **TCP Service Protocol:**
   You must write a Bash script (e.g., using `socat` or `ncat`) that listens on `TCP port 9000`.
   - The client will connect and send a single line request: `ARCHIVE <YYYY-MM-DD>`.
   - The server must find the corresponding log file, extract the CRITICAL multi-line records, write them to a temporary file, and compress it using `/app/arc_tool`.
   - The server must then respond to the client with:
     `SUCCESS <byte_size_of_compressed_file>\n`
     followed immediately by the raw binary bytes of the compressed `.arc` file.
   - If the log file for the requested date does not exist, the server should respond with: `ERROR NOT_FOUND\n` and close the connection.

Please implement and start this server in the background. Write a log of all incoming requests to `/home/user/server.log` in the format: `[YYYY-MM-DD HH:MM:SS] REQUESTED: <YYYY-MM-DD> - STATUS: <SUCCESS|ERROR>`.

Ensure your server is running and listening on port 9000 before finishing the task.
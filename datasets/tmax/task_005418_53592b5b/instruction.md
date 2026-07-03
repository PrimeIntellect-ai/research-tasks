As a technical writer, I am organizing documentation from multiple automated systems. Sometimes, buggy upstream extractors generate paths that attempt to escape the documentation directory (similar to a zip-slip vulnerability, e.g., using `../`). 

I need you to write a C++ program that watches an incoming directory, parses multi-line log records, filters out malicious paths, and streams the valid results to a consolidated index.

Here are the specific requirements:
1. Create a C++ program at `/home/user/watcher.cpp` and compile it to `/home/user/watcher` (use `g++ -O2`).
2. The program must use Linux `inotify` to monitor the directory `/home/user/incoming_docs/` for `IN_CLOSE_WRITE` events.
3. When a file triggers the event, the program should open the file using C++ streaming I/O (`std::ifstream`) and parse its multi-line records. 
4. The records in the incoming files are formatted strictly as follows:
   ```
   RECORD_START
   Path: <filepath>
   Title: <document title>
   RECORD_END
   ```
   There may be empty lines between records.
5. **Security Filter:** The program must ignore any record where the `<filepath>` contains the substring `../` (directory traversal attempt).
6. For every valid record (no `../` in the path), append a line to `/home/user/clean_index.txt` in exactly this format:
   `<filepath> | <document title>`
7. The program should run continuously until killed. Make sure it flushes its output file stream after processing a newly dropped file.

**Execution Steps:**
1. Write and compile the C++ program.
2. Start the `./watcher` program in the background.
3. Copy the pre-existing test file `/home/user/test_data.log` into the incoming directory: `cp /home/user/test_data.log /home/user/incoming_docs/trigger.log`
4. Wait a couple of seconds for the background process to detect and process the file.
5. Kill the background watcher process.
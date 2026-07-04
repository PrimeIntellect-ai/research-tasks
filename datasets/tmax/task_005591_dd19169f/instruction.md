You are helping me organize a messy C project workspace. I have a large build log file containing multi-line error and warning records, and I need to quickly categorize the source files that are causing these issues without duplicating their contents on disk.

Here is what you need to do:

1. **Analyze the Log:**
   There is a log file located at `/home/user/build.log`. It contains multi-line records formatted strictly like this:
   ```
   BEGIN_RECORD
   TYPE: [FATAL|WARN|INFO]
   SRC: [absolute path to source file]
   DETAILS: [error message]
   END_RECORD
   ```

2. **Write a C Parser:**
   Write a C program at `/home/user/parser.c` that parses this log file. 
   - **Requirement:** You *must* use memory-mapped I/O (`mmap`) to read the file, simulating high-performance streaming/parsing of large logs. Standard `fopen`/`fread` are not allowed for reading the log file.
   - The program should scan for records of type `FATAL` and `WARN`.

3. **Organize Source Files using Links:**
   Based on the parsed log, your C program should automatically categorize the source files (or generate and execute a shell script to do so).
   - First, ensure the directories `/home/user/fatal_errors` and `/home/user/warn_errors` exist.
   - For every `FATAL` record, create a **hard link** of the source file (`SRC`) inside `/home/user/fatal_errors/`, keeping the original filename (e.g., `/home/user/src/main.c` becomes a hard link at `/home/user/fatal_errors/main.c`).
   - For every `WARN` record, create a **symbolic link** (symlink) of the source file (`SRC`) inside `/home/user/warn_errors/`, keeping the original filename.

4. **Execution:**
   Compile your C code to `/home/user/parser` and run it. When the program finishes, the directories `/home/user/fatal_errors` and `/home/user/warn_errors` should be correctly populated with the hard and symbolic links respectively. 

Make sure your C program handles potential missing source files gracefully (skip them if they don't exist on disk).
I need you to help organize and format some project files. We have a system that writes binary log files (`.binlog`), and I need a C utility to safely read these files and convert them to JSON, even while the system might be concurrently writing to them.

First, fix the `cJSON` library we have vendored at `/app/vendor/cJSON`. It's version 1.7.15, but someone messed up the `Makefile` and it won't build the shared library `libcjson.so` properly. You'll need to find the error in the Makefile, fix it, and build the shared library.

Next, write a C program at `/home/user/log_converter.c` and compile it to `/home/user/log_converter` (dynamically linked against the fixed `libcjson.so`). 

Your C program must do the following:
1. Accept a single file path as a command-line argument.
2. Open the file and acquire a shared (read) lock using `fcntl()` to prevent race conditions with the writer (which holds an exclusive write lock).
3. Read the binary log file. The file consists of a sequence of the following C struct (tightly packed, no padding):
   ```c
   #pragma pack(push, 1)
   struct LogEntry {
       uint32_t timestamp;
       uint8_t level; // 0=DEBUG, 1=INFO, 2=WARN, 3=ERROR
       char message[64]; // Null-terminated string, may be padded with zeroes
   };
   #pragma pack(pop)
   ```
4. Convert each struct into a JSON array of objects using the `cJSON` library. Each object should have keys: `"time"`, `"lvl"` (as integer), and `"msg"` (as string).
5. Print the unformatted (minified) JSON array to `stdout` and exit.
6. Release the lock and close the file.

Constraints:
- You must use `cJSON_PrintUnformatted` for the output.
- The program must block until the read lock is acquired if the writer currently has it locked.

Once compiled, our test suite will execute your `/home/user/log_converter` against thousands of randomly generated binary log files to ensure strict bit-for-bit equivalence with our reference implementation.
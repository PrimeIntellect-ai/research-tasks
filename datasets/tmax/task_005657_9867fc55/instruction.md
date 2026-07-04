You are a developer debugging a failing build pipeline in `/home/user/project`. 

When you run `./build.sh`, it compiles `processor.c` and runs it against a binary serialization file `data.bin`. The `processor` reads Type-Length-Value (TLV) encoded records from `data.bin`. However, the build is currently failing because `processor` crashes with a segmentation fault (buffer overflow) when it encounters a specific malformed or oversized record.

Your tasks are to:
1. Debug `processor.c` and `data.bin` to determine exactly which record (0-indexed) is causing the buffer overflow.
2. Create a file `/home/user/project/crash_info.txt` and write just the single integer representing the 0-indexed record number that triggers the crash.
3. Fix the buffer overflow vulnerability in `processor.c`. The fixed program must successfully read all records (including the oversized one) without crashing. For oversized records, it is acceptable to truncate the parsed string to fit within the buffer, provided the file pointer is correctly advanced so subsequent records are read correctly.
4. Run `./build.sh` successfully. The script should exit with code 0 and generate a `build_status.txt` file containing "Build Success".

All files are located in `/home/user/project`. You must use standard C and shell debugging tools (e.g., `gdb`, `xxd`, `hexdump`) to solve this.
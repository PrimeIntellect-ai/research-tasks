You are tasked with debugging a failing build and test pipeline for a C data processing utility. 

You have a project located at `/home/user/project/` containing a C source file `data_parser.c` and a test script `test_all.sh`. The test script compiles the program and runs it against a batch of input files located in `/home/user/inputs/`.

Currently, running `/home/user/project/test_all.sh` fails because the program crashes on one specific, malformed input file, but the script suppresses standard error and doesn't tell you which file caused the crash. 

Your objectives are:
1. Identify the specific input file that causes the segmentation fault.
2. Use system call tracing (e.g., `strace`) on the failing run to identify the exact system call used to open the input file right before the crash.
3. Fix the underlying memory issue (buffer overflow) in `/home/user/project/data_parser.c`. You should make the buffer large enough to safely hold the data being read, or restrict the read size to the buffer's capacity.
4. Run `/home/user/project/test_all.sh` successfully. When successful, it will automatically generate a file at `/home/user/project/pass.flag`.
5. Create a report file at `/home/user/resolution.txt` containing exactly three lines:
   - Line 1: The absolute path of the input file that caused the crash.
   - Line 2: The name of the system call (e.g., `open` or `openat`) used to open that file in the trace.
   - Line 3: The C function name where the vulnerability was located.

Example `/home/user/resolution.txt`:
/home/user/inputs/input_099.dat
openat
process_data
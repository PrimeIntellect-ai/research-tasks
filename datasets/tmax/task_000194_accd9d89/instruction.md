You are tasked with debugging a regression in a C project using bisection, system call tracing, and memory dump analysis. 

A local Git repository for an image processing tool is located at `/home/user/image_processor`. 
The repository has 200 commits. The commit tagged `v1.0` is known to be good, and the commit tagged `v2.0` is known to be bad. 
At some point between these tags, a bug was introduced that causes the program to crash (abort) and drop a simulated memory dump file named `mem_dump.bin`. 

Your objectives are:
1. **Delta Debugging (Bisection):** Use `git bisect` along with a bash test script to automatically find the first bad commit. The build command is simply `gcc -o img_proc main.c`. The program is expected to run successfully (exit code 0) without dropping a `mem_dump.bin` file.
2. **System Call Tracing:** Run the compiled buggy program (`img_proc`) at the *first bad commit* using `strace`. Save the complete standard error output of `strace` to `/home/user/syscalls.log`.
3. **Memory Dump Analysis:** The buggy program produces a `mem_dump.bin` file when it crashes. At the *first bad commit*, use string extraction utilities (e.g., `strings`) to analyze `mem_dump.bin`. You will find a corrupted filename prefixed with `CONFIG_STR: `. Extract *only* the corrupted filename (not the prefix) and save it to `/home/user/corrupted_filename.txt`.
4. **Result Reporting:** Save the full Git commit hash of the first bad commit to `/home/user/bad_commit.txt`.

Constraints:
- You must use Bash shell commands and standard Linux CLI utilities (e.g., `git`, `strace`, `strings`, `grep`, `awk`).
- Do not use Python or other scripting languages to solve the problem.
- Ensure your test script for `git bisect` cleans up compiled binaries and dump files between runs.
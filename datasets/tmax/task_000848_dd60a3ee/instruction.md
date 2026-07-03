You are tasked with debugging a regression in a C project using `git bisect` and a debugger (like `gdb` or core dump analysis).

There is a Git repository located at `/home/user/parser_repo`. 
A wrapper script located at `/home/user/test.sh` compiles and runs the program with a specific input (`"data file.txt"`, simulating a filename with spaces). 

Recently, the C program started segfaulting when encountering filenames with spaces. The `test.sh` script currently crashes with a segmentation fault on the `HEAD` of the `main` branch, but it worked fine in the initial commit.

Your objectives:
1. Use `git bisect` to find the exact commit hash that introduced the segmentation fault. Write the full, 40-character commit hash to `/home/user/bad_commit.txt`.
2. Analyze the crash (e.g., using `gdb` or generating a core dump) at the exact bad commit. Identify the name of the C function where the segfault occurs. Write the exact function name to `/home/user/crash_function.txt`.
3. Identify the line number in `main.c` where the segmentation fault occurs in the *bad commit*. Write just the integer line number to `/home/user/crash_line.txt`.

Ensure your final answers are saved in the specified files before finishing.
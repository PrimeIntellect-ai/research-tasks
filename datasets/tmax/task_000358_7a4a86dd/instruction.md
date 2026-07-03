You have been given access to a messy, buggy C project located in `/home/user/project`. This project implements a basic state-machine based HTTP request parser. The original developer struggled with memory management (pointer lifetimes) and file organization, resulting in a project that compiles but produces completely incorrect output.

Your goal is to fix the memory issues, reorganize the project, and create a benchmarking script.

Phase 1: Project Organization
1. Create two new directories: `/home/user/project/src` and `/home/user/project/include`.
2. Move all `.c` files into the `src` directory.
3. Move all `.h` files into the `include` directory.
4. Modify the existing `/home/user/project/Makefile` so that it correctly compiles the project from these new directories. The output binary must be named `http_parser` and placed in `/home/user/project/`.

Phase 2: Fix the Parser
The file `parser.c` (now in your `src` directory) contains a critical memory lifetime bug. The function `parse_requests` reads lines from a file into a local stack buffer and assigns pointers to this buffer directly to the `Request` structs. As a result, all stored requests end up pointing to the last read line (or garbage data).
1. Fix the bug in `parser.c` so that the `Method`, `URI`, and `Version` strings are properly duplicated/allocated in memory for each parsed request.
2. Ensure that the memory is correctly freed in the `free_requests` function to prevent memory leaks. 
3. Do not change the standard output format of the program; it should continue to print `"Method: [method], URI: [uri], Version: [version]"` for each valid request.

Phase 3: Benchmarking & Sorting
1. Create a bash script at `/home/user/project/benchmark.sh`.
2. The script must be executable.
3. When executed, the script must:
   a. Run `make clean` and `make` to ensure the `http_parser` binary is up to date.
   b. Use the `time` command (or `time` shell keyword) to run the `http_parser` binary on `/home/user/project/requests.log`.
   c. Capture the standard output of the `http_parser`, sort the output alphabetically (using the `sort` command), and save the sorted output to `/home/user/project/sorted_output.txt`.

Ensure your C code fixes compile without warnings using standard `gcc`. All file paths you reference should be absolute where possible, or strictly relative to `/home/user/project/`.
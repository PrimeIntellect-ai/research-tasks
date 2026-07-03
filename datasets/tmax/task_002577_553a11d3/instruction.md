You are helping a developer organize a chaotic directory of test inputs for a high-performance mathematical library. 

In `/home/user/math_lib.c`, there is a C function with the following signature:
`int compute_collatz_steps(int n);`
This function computes the number of steps required to reach 1 in the Collatz conjecture for a given positive integer `n`.

In `/home/user/test_data/`, there are several JSON files. Each file is named `test_<id>.json` and contains a simple JSON object: `{"id": <id>, "value": <n>}`.

Your task is to organize these test files into categorized subdirectories based on the number of Collatz steps their `value` requires, and to create an end-to-end orchestration script.

Please do the following:
1. Write a script in the language of your choice (e.g., Python, Node.js, Ruby) that:
   - Uses Foreign Function Interface (FFI) / cross-language interop to load the compiled C library (`/home/user/libmath.so`) and call `compute_collatz_steps`.
   - Parses the JSON files in `/home/user/test_data/`.
   - Evaluates the `value` from each JSON file using the C function.
   - Moves the JSON file into a new directory structure: `/home/user/organized_data/<steps>/test_<id>.json`, where `<steps>` is the integer returned by the C function.
   
2. Create a bash script at `/home/user/orchestrate.sh` that orchestrates this entire process from end-to-end:
   - Compiles `/home/user/math_lib.c` into a shared library `/home/user/libmath.so`.
   - Creates the `/home/user/organized_data/` directory.
   - Runs your FFI script to categorize and move the files.
   - Generates a summary CSV file at `/home/user/summary.csv` containing the distribution of the files. The CSV must have the header `steps,file_count`. Each subsequent row should list the directory name (which corresponds to the number of steps) and the number of files in that directory. The CSV must be sorted numerically by the `steps` column.

Make sure `/home/user/orchestrate.sh` is executable and run it to complete the task. Do not delete the original C source file.
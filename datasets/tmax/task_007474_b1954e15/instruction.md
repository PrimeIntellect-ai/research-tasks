You are a QA Engineer setting up a cross-language automated test environment. Your team has identified performance bottlenecks in python-based data processing, so you need to implement a core utility in C, expose it via Foreign Function Interface (FFI), and write a test harness to verify its correctness against golden records.

Your objective is to complete the following steps:

1. Create a working directory at `/home/user/qa_env`.
2. Create two input test files in `/home/user/qa_env/inputs/`:
   - `file1.txt` containing the lines:
     `zebra`
     `apple`
   - `file2.txt` containing the lines:
     `mango`
     `banana`
3. Write a C source file at `/home/user/qa_env/sorter.c` containing a function with the following signature:
   `int process_data(char **files, int num_files, char *out_file);`
   This function must:
   - Read all text lines from the provided list of file paths.
   - Strip any trailing newline characters from each line.
   - Sort all the combined lines lexicographically (alphabetically).
   - Hex-encode each sorted string (e.g., "apple" -> "6170706c65").
   - Write the hex-encoded strings, one per line, to the specified `out_file`.
   - Return 0 on success, or -1 on failure.
4. Compile `sorter.c` into a shared library named `/home/user/qa_env/libqa.so`.
5. Create a golden master file at `/home/user/qa_env/golden.txt` containing the expected correct hex-encoded output of the sorted lines.
6. Write a Python test script at `/home/user/qa_env/test_runner.py` that:
   - Uses the `ctypes` library to load `libqa.so`.
   - Calls the `process_data` function, passing it the paths to `file1.txt` and `file2.txt`, and instructs it to write to `/home/user/qa_env/output.txt`.
   - Uses the system's `diff` command (via `subprocess` or `os.system`) to compare `output.txt` and `golden.txt`.
   - Redirects the output of the `diff` command to `/home/user/qa_env/test_result.log`.
7. Execute `test_runner.py` so that `output.txt` and `test_result.log` are generated.

If everything is implemented correctly, `test_result.log` should be empty (indicating no differences).
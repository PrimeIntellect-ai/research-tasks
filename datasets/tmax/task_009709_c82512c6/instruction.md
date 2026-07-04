You are a security researcher investigating a suspicious application left behind on a compromised server. The application consists of a Python wrapper and a compiled binary decoder.

You have been provided a Git repository located at `/home/user/decoder_project`. 

Your investigation has three objectives:

1. **Regression Analysis (Git Bisection):**
   The Python script `analyze.py` in the repository processes a set of data files. Originally, it worked perfectly. However, a recent commit introduced a concurrency bug (a race condition caused by multithreading without proper locking) that causes data loss when appending results to a global list.
   Use Git bisection to find the exact commit hash that introduced this race condition. Write the full 40-character commit hash to `/home/user/bad_commit.txt`.

2. **Binary Reverse Engineering:**
   The Python script relies on a compiled binary named `decoder.bin` (located in the repository root) to process files. This binary requires a secret key passed as the first argument, or it will refuse to decode. The developers hardcoded this key inside the binary.
   Analyze `decoder.bin` to extract the hardcoded secret key. Write the exact key string to `/home/user/secret_key.txt`.

3. **Corrupted Input Handling & Fix:**
   Inside `/home/user/decoder_project/inputs/`, there are 100 text files. A few of these files contain corrupted edge-case data that causes `decoder.bin` to crash/panic (abort). 
   Write a new Python script at `/home/user/secure_runner.py` that:
   - Uses `concurrent.futures.ThreadPoolExecutor` with exactly 4 workers to process all `.txt` files in the `inputs/` directory concurrently.
   - Calls `./decoder.bin <SECRET_KEY> <FILE_PATH>` for each file.
   - Gracefully catches and ignores any crashes/panics from the binary (ignoring corrupted files).
   - Uses a proper locking mechanism (e.g., `threading.Lock`) to safely collect the standard output of the successful executions into a global Python list.
   - Writes the successfully decoded lines as a JSON array of strings to `/home/user/output.json`.

Ensure your final scripts are fully functional. You may use standard Linux terminal tools (`strings`, `objdump`, `ltrace`, `strace`, `gdb`, etc.) and Python.
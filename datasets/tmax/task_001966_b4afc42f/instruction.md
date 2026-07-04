I am migrating a legacy data processing pipeline from Python 2 to Python 3, and I need to significantly improve its performance. The pipeline reads a binary file containing thousands of 32-bit signed integers (little-endian) and finds the top 5 most frequent integers. 

To achieve maximum performance, I want to replace the pure-Python counting logic with a custom C library, and use Python 3 to orchestrate the process via `ctypes`.

Here is what you need to do:

1. **Write the C Library (`/home/user/counter.c`)**
   - Implement a custom hash table (or similar data structure) to count the occurrences of integers.
   - It must expose the following functions (with C linkage):
     - `void init_counter()`: Initializes/clears the data structure.
     - `void add_values(const int* data, int count)`: Takes an array of integers and its length, and adds them to the counts.
     - `int get_count(int value)`: Returns the count for a specific integer.
   - **Conditional Build**: The code must check for a preprocessor macro `FAST_MODE`. If `FAST_MODE` is defined, the internal hash table capacity should be at least 8192. Otherwise, it should be 1024.

2. **Build the Shared Library**
   - Compile `/home/user/counter.c` into a shared library at `/home/user/libcounter.so`.
   - You must compile it with the `-DFAST_MODE` flag enabled, alongside `-fPIC` and `-shared`.

3. **Write the Python 3 Script (`/home/user/migrate.py`)**
   - Use the `ctypes` module to load `/home/user/libcounter.so`.
   - Read the binary data from `/home/user/data.bin` (which contains contiguous 32-bit signed integers in little-endian format).
   - Call `init_counter()`.
   - Pass the parsed integers to `add_values`.
   - Using the Python script (and `get_count` if needed, or by tracking unique values in Python), determine the top 5 most frequent integers. If there is a tie in frequencies, prioritize the larger integer value.
   - Write these top 5 integers to `/home/user/result.txt`, one per line, in descending order of frequency.

4. **Benchmarking Output**
   - To indicate the completion of the benchmarking phase, the Python script must write a JSON file to `/home/user/benchmark.json` with the exact contents:
     ```json
     {"status": "success", "language": "python3+C"}
     ```

Assume `/home/user/data.bin` already exists. Write the C code, build it, write the Python script, and execute it to generate the outputs.
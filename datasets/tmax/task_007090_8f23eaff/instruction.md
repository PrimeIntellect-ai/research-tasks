You are a script developer working on a text processing utility. We have an existing C++ implementation of a basic Run-Length Encoding (RLE) function, but it has severe memory safety issues (buffer overflows) and isn't accessible from our Python scripts.

Your task is to fix the memory safety issues, generate a patch, compile it as a shared library, and write a Python wrapper to benchmark and test it.

Here is the initial file `/home/user/rle.cpp`:
```cpp
void rle_encode(const char* input, char* output, int max_out_len) {
    int i = 0;
    int j = 0;
    while (input[i] != '\0') {
        int count = 1;
        while (input[i] == input[i+1] && count < 9) { // count < 9 keeps it to a single digit
            count++;
            i++;
        }
        output[j++] = input[i];
        output[j++] = count + '0';
        i++;
    }
    output[j] = '\0';
}
```

Requirements:
1. Fix the undefined behavior / buffer overflow in `/home/user/rle.cpp`. The function must strictly respect `max_out_len`, ensuring that it never writes past `output[max_out_len - 1]`. The output must always be null-terminated. Truncate the encoding if the buffer is too small.
2. Expose the `rle_encode` function with C linkage (`extern "C"`) so it can be called via Foreign Function Interface (FFI).
3. Generate a unified diff of your changes against the original file and save it to `/home/user/rle.patch`.
4. Compile the fixed `/home/user/rle.cpp` into a shared library named `/home/user/librle.so` (ensure it is compiled with position-independent code).
5. Write a Python script `/home/user/ffi_test.py` that uses the `ctypes` module to load `/home/user/librle.so`. The script must:
   - Create a string buffer of size exactly `10`.
   - Call `rle_encode` with the input string `"WWWWWWWWWWWWBWWWWWWWWWWWW"`, the buffer, and `10` as the maximum length.
   - Print the resulting encoded string to standard output.
6. Write a bash script `/home/user/benchmark.sh` that executes the Python script 50 times in a loop, measuring the total real execution time using the `time` command (or similar bash built-ins), and appends the total time to `/home/user/benchmark.log`.

Make sure all created files are located in `/home/user/` and have the appropriate permissions. Do not change the function signature of `rle_encode`.
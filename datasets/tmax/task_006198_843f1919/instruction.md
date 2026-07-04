You are a systems programmer working on a polyglot mathematical encoding project. We have a C library that performs a custom mathematical transformation on character data, a Go program that concurrently processes bulk data using this library, and we need a Python test fixture to verify the C library's correctness. 

Currently, the C library fails to build due to a linker issue, which is blocking the entire pipeline. 

Your tasks:
1. **Fix the Build System**: Inspect `/home/user/project/Makefile` and `/home/user/project/mathcodec.c`. The compilation of `libmathcodec.so` fails due to a linking issue (hint: it uses math functions). Fix the `Makefile` so that running `make` successfully produces `libmathcodec.so`.
2. **Write a Python Test Fixture**: Write a Python script at `/home/user/project/test_codec.py`. This script must:
   - Use the `ctypes` module to load `/home/user/project/libmathcodec.so`.
   - Setup a test fixture that passes the exact UTF-8 byte string `"TEST"` to the C function `void encode(const char* input, double* output, int len)`.
   - The function populates the `output` array with floating point numbers.
   - For each of the 4 characters, format the resulting float to exactly 3 decimal places.
   - Write these 4 formatted floats, comma-separated (e.g., `1.234, 5.678, ...`), to `/home/user/project/python_test_out.txt`.
3. **Run the Polyglot Pipeline**:
   - Run `make` to build the shared library.
   - Run your `test_codec.py` script.
   - Build the provided Go program `processor.go` which uses concurrency (goroutines/channels) via cgo to process `/home/user/project/input.txt`. Output the binary as `processor`.
   - Run `./processor /home/user/project/input.txt /home/user/project/output.txt`. Note: You must run this with `LD_LIBRARY_PATH=/home/user/project`.

Ensure all output files (`python_test_out.txt` and `output.txt`) are generated successfully.
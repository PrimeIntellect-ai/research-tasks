I am building a high-performance feature for our web backend to compute checksums of large incoming payload streams. To handle the throughput, we decided to use a fast C-based checksum library wrapped in a concurrent Go module, which is then called from our Python backend.

However, the build process is broken, and I need you to fix it and write the final Python integration script.

Here is the setup:
1. We have a vendored C library located at `/app/fastcrc-1.0`. It contains a Makefile, but running `make` and then trying to link it later fails. Fix the Makefile so that it produces a static library (`libfastcrc.a`) suitable for inclusion in a shared library.
2. We have a Go wrapper located at `/app/gocrc`. It uses cgo to include `libfastcrc.a` and exposes a concurrent checksum calculation function via C ABI. Build this Go package into a shared library named `libgocrc.so` in the `/app/gocrc` directory.
3. Write a Python script at `/home/user/process_uploads.py` that uses `ctypes` to load `/app/gocrc/libgocrc.so`. 
4. The Go library exposes a function: `unsigned int CalculateCRC(char* data, int length);`. 
5. Your Python script must read the binary file `/app/test_payload.bin` into memory, pass it to the Go `CalculateCRC` function via `ctypes`, and print ONLY the resulting integer checksum to standard output.

For this feature to be accepted, your Python integration must achieve a performance speedup of at least 1.5x over our baseline Python implementation located at `/app/baseline.py`. 
Please ensure the Python script `/home/user/process_uploads.py` is executable and correct.
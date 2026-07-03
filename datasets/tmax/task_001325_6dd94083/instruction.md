You are a systems programmer debugging a C library linking issue and building a test for it. 

You have been given a workspace at `/home/user/project` with the following files:
1. `checksum.c`: Contains a simple custom checksum function.
2. `Makefile`: A broken makefile intended to build a shared library `libchecksum.so`.
3. `message.proto`: A Protocol Buffers definition file containing a `Record` message.

Your task is to:
1. Fix the `Makefile` so that it successfully builds `libchecksum.so` as a valid shared library (currently it fails due to missing position-independent code and shared library flags).
2. Run `make` to build the library.
3. Compile the `message.proto` file into Python code using the `protoc` compiler.
4. Write a Python test script named `/home/user/project/run_test.py` that does the following:
   - Imports the generated protobuf module.
   - Creates a `Record` message, setting `id` to `42` and `name` to `"SystemsDebug"`.
   - Serializes the message to raw bytes.
   - Uses the `ctypes` module to load `./libchecksum.so`.
   - Calls the `compute_checksum(const char* data, int len)` C function, passing the serialized protobuf bytes and its length.
   - Writes the returned integer checksum (as a string) to `/home/user/project/checksum_out.txt`.

Ensure your Python script correctly defines the `argtypes` and `restype` (which is `uint32_t`) for the C function. Run your test script to produce the output file.
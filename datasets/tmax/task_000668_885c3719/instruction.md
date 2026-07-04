You are a platform engineer responsible for maintaining our CI/CD pipelines. As part of a new release process, our pipeline needs to encode build artifacts before publishing them. For performance reasons, the encoding algorithm is implemented in C, but our pipeline orchestration is written in Python.

Currently, the pipeline is broken. You need to fix the C project's build, write the Python FFI wrapper, and process the mock artifacts.

Here are your instructions:

**Phase 1: Fix the C Build**
The C library is located in `/home/user/artifact_encoder/`. It contains `encoder.c`, `encoder.h`, and a `Makefile`. 
However, the `Makefile` is incorrectly configured to build an executable instead of a shared library, and it currently fails to link because there is no `main` function.
Fix the `Makefile` so that running `make` in `/home/user/artifact_encoder/` compiles the C code into a shared library named `libencoder.so`. Ensure you use the correct compiler flags for generating position-independent code and a shared object.

**Phase 2: Write the Python FFI Script**
Create a Python script at `/home/user/pipeline/process_artifacts.py`. 
This script must use the built-in `ctypes` module to load the `libencoder.so` shared library you just built.

The C library exposes the following function:
`int process_data(const unsigned char* input, int length, unsigned char* output);`
*(It processes `length` bytes from `input`, writes the encoded bytes to `output`, and returns the number of bytes processed).*

Your Python script must:
1. Iterate through all files in the directory `/home/user/pipeline/raw_artifacts/`.
2. Read the raw bytes from each file.
3. Use the `process_data` C function to encode the bytes.
4. Write the encoded bytes to `/home/user/pipeline/encoded_artifacts/` using the original filename with a `.enc` suffix (e.g., `data.bin` becomes `data.bin.enc`).
5. Write a summary log to `/home/user/pipeline/status.log` containing exactly the following text: `Total bytes processed: X` (where X is the integer sum of the sizes of all processed files).

Make sure your Python script manages memory correctly with `ctypes` (e.g., creating properly sized string buffers for the output). Run your Python script to process the files and generate the log.
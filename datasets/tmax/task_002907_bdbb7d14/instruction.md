I'm working on a data processing pipeline that relies on a legacy C library for high-performance string formatting, but the project is currently in a broken state. It looks like a classic case of dependency and configuration rot, similar to a Node.js project failing due to peer dependency conflicts, but here we are dealing with C shared libraries and Python ABI wrappers.

Your goal is to organize, fix, and run this data processing project located in `/home/user/project`.

Here is the current state of the project and what you need to do:

1. **Build System & Linking:**
   The `Makefile` in `/home/user/project/src/Makefile` is broken. It is supposed to compile `processor.c` into a shared library named `libprocessor.so` and place it in `/home/user/project/lib/`. However, it's missing the necessary compiler flags to create a shared object (ABI management), and the output directory is not explicitly created by the Makefile. Fix the Makefile and build the library.

2. **Code Translation (ABI):**
   The C library exposes a function `void process_record(struct Record* rec, char* out_buf);`.
   The `struct Record` is defined in `src/processor.c` as:
   ```c
   struct Record {
       int32_t id;
       float value;
       char name[16];
   };
   ```
   Open `/home/user/project/scripts/process.py` and translate this C struct into a Python `ctypes.Structure` so that the Python script can correctly pass data to the shared library. Complete the `TODO` sections in the Python script.

3. **Checksum & Data Validation:**
   The directory `/home/user/project/data/` contains several binary files (`.dat`). Some of these files are corrupted. 
   Each file has a strict format: The first 4 bytes are a little-endian unsigned 32-bit integer representing the CRC32 checksum of the *rest* of the file. 
   Update `scripts/process.py` to read each file, extract the checksum, and compute the CRC32 of the remaining bytes using `zlib.crc32`. 
   *Only* parse and process the file if the checksums match. If they match, unpack the remaining 24 bytes directly into the `Record` structure.

4. **Execution:**
   Run the `process.py` script. For every valid file, the C library will format the record into a string and populate the `out_buf`. 
   Append every successfully processed string (which will be null-terminated by the C library) to `/home/user/project/output.log`, with each string on a new line.

Constraints:
- Do not modify `src/processor.c`.
- Ensure your Python script skips the files with invalid checksums automatically.
I'm organizing a massive, legacy project repository and I need a high-performance indexer to catalog binary assets. I downloaded the source for `xxhash` to use its fast hashing, but I'm having trouble getting it to build and integrate properly.

Here is what I need you to do:

1. **Fix and Compile the Vendored Library:**
   There is a vendored copy of the `xxhash` source code located at `/app/vendored/xxhash-0.8.2`. However, the `Makefile` has been tampered with and currently fails to build the shared library. Find the deliberate perturbation in the `Makefile` (look at how the `CC` variable or compilation targets are defined), fix it, and compile the library to produce `libxxhash.so`. 

2. **Clean the File List:**
   I have a poorly formatted list of legacy file paths in `/home/user/raw_file_paths.txt`. Many lines have broken formatting, extra spaces, or are commented out with `#`. Use shell utilities to perform a large-scale text cleanup:
   - Remove all lines starting with `#` (ignoring leading whitespace).
   - Strip leading and trailing whitespace from all lines.
   - Remove any empty lines.
   - Save the cleaned list to `/home/user/clean_paths.txt`.

3. **Implement the Fast Indexer (`/home/user/indexer.py`):**
   Write a Python script that takes a single positional argument (a file path). The script must:
   - Use the `mmap` module to memory-map the file for high-performance I/O.
   - Extract the first 4 bytes of the file (the magic header) and format it as a lowercase hex string (e.g., `89504e47`). If the file is less than 4 bytes, pad the hex string with trailing zeros (e.g., a 2-byte file `ff d8` becomes `ffd80000`).
   - Use the Python `ctypes` module to load your freshly compiled `/app/vendored/xxhash-0.8.2/libxxhash.so`.
   - Pass the memory-mapped file buffer to the `XXH64` C function to compute the 64-bit xxhash of the *entire* file contents. Use `0` as the seed.
   - Print a single line to standard output in exactly this format: `<file_path> <4-byte-hex-header> <xxhash64-hex-lowercase>`

Ensure your script is executable (`chmod +x /home/user/indexer.py`) and has `#!/usr/bin/env python3` at the top. It must process files efficiently using memory mapping and directly calling the C library, without installing any additional Python packages via pip.
You are tasked with implementing a high-performance, concurrency-safe configuration archiver in C++.

We have a system where a background process constantly updates a large JSON configuration file (`/home/user/config/live.json`). You need to write a C++ program that safely creates compressed backups of this configuration file without corrupting the data or blocking the writer for too long.

Here are the requirements:
1. **Fix the Vendored Compression Library**:
   We have vendored the `miniz` (v3.0.2) compression library at `/app/miniz-3.0.2/`. It contains `miniz.c`, `miniz.h`, and a `Makefile`. However, the build is broken due to an intentional misconfiguration. Inspect the `Makefile`, fix the perturbation, and compile it into a static library (`libminiz.a`).

2. **Implement the Archiver (`/home/user/safe_archiver.cpp`)**:
   Write a C++ program that takes two arguments: `<input_file>` and `<output_dir>`.
   It should perform exactly **50 iterations** of the following process:
   - Open the `<input_file>`.
   - Acquire a shared (read) lock using `flock()` to ensure you don't read a partially written file.
   - Use **memory-mapped I/O** (`mmap`) to map the file into memory for maximum read performance.
   - Use the `miniz` library to compress the mapped memory directly into a new zip archive in `<output_dir>`, named `snap_<iteration_number>.zip` (e.g., `snap_0.zip`, `snap_1.zip`, ..., `snap_49.zip`). You must use `miniz`'s C API (e.g., `mz_zip_add_mem_to_archive_file_in_place`).
   - Unmap the memory, release the lock, and close the file.
   - Sleep for 10 milliseconds (`usleep(10000)`) between iterations.

3. **Compilation**:
   Compile your program to `/home/user/safe_archiver`. You must link it against the fixed `libminiz.a` and use standard optimization flags (`-O3`).

The system will run a multi-threaded Python writer against `/home/user/config/live.json` while simultaneously executing your `/home/user/safe_archiver`. 

Your solution will be evaluated on a strict numerical metric: **Valid Snapshot Throughput**. 
- Any snapshot containing malformed JSON (due to race conditions from failing to lock) will result in heavy penalties.
- Using standard `read()` instead of `mmap`, or failing to fix the `miniz` compilation flags, will result in the program failing to meet the minimum throughput threshold.
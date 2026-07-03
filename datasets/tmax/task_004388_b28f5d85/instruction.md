You are an artifact manager tasked with curating a large local binary repository. Our artifact system uses a custom format: a proprietary 16-byte binary header followed immediately by a standard ZIP archive. 

We have a massive directory of these artifacts at `/home/user/repo`. Some of the artifacts are corrupted (either the header is wrong or the ZIP archive fails integrity checks). 

We have a vendored C++ library to help with archive extraction at `/app/vendor/libarchive_custom`. However, a recent refactor broke its build system, and it currently fails to compile or link correctly. 

Your tasks are:
1. Fix the vendored package at `/app/vendor/libarchive_custom` so that it builds and installs successfully to `/app/vendor/install`.
2. Read the configuration file at `/home/user/repo_config.json`. This file specifies:
   - `target_dir`: The root directory to scan (e.g., `/home/user/repo`).
   - `expected_magic`: A hex string of the first 4 bytes expected in every valid artifact header.
3. Write a C++ program at `/home/user/artifact_scanner.cpp` that:
   - Recursively traverses the `target_dir`.
   - Opens every `.art` file.
   - Extracts the 16-byte header and verifies the first 4 bytes match the `expected_magic`.
   - Uses the fixed `libarchive_custom` library to verify the integrity of the ZIP payload (starting at byte offset 16).
4. Your C++ program must output a report to `/home/user/scan_results.csv` with the format: `filepath,status`, where status is `VALID`, `BAD_HEADER`, or `CORRUPT_ARCHIVE`.
5. **Performance Requirement:** The repository is huge. We have provided a slow, single-threaded Python reference implementation at `/home/user/reference_scanner.py`. Your C++ implementation must be highly optimized (consider using `std::filesystem`, memory mapping, or multithreading) to achieve a speedup of at least **3.0x** over the reference implementation. Compile your binary to `/home/user/artifact_scanner`.

To complete the task:
- Ensure the library is fixed and your code compiles.
- Run your optimized scanner to generate the CSV.
- Ensure your scanner finishes quickly enough to meet the performance threshold.
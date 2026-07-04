I am organizing a data processing project that analyzes software dependencies. I have a large dataset of raw semantic versions in `/home/user/versions.txt` (100,000 lines). I need to parse and sort them, but native Python is too slow for our CI pipeline. 

I decided to use a fast C library for semantic version comparison. I vendored the `semver.c` library by `h2non` into `/app/semver.c-1.0.0`. However, the CI is currently failing for two reasons:
1. Our test suite passes locally on small test cases, but when run against the full dataset, the C library causes a segmentation fault. I suspect there is a memory safety issue or undefined behavior when handling long pre-release tags or build metadata.
2. The project directory is currently a mess, and everything is dumped in `/home/user`.

Here is what I need you to do:
1. **Fix the C library**: Investigate `/app/semver.c-1.0.0/semver.c` and fix the memory safety issue that causes crashes on long strings. 
2. **Build the shared library**: Compile the fixed C library into a shared object (`libsemver.so`). Ensure it is compiled with `-O3` optimizations for maximum speed.
3. **Reorganize the project**: Create a clean directory structure under `/home/user/project/`. Move things exactly as follows:
   - Your Python code should go into `/home/user/project/src/`
   - The compiled shared library should go into `/home/user/project/lib/`
   - Move the dataset to `/home/user/project/data/versions.txt`
4. **Implement the Python sorter**: Write a Python script `/home/user/project/src/sort_versions.py` that reads `/home/user/project/data/versions.txt`. It must use `ctypes` to load `libsemver.so` and bind to its version comparison function (e.g., `semver_compare`). Use this C function as the sorting key/comparator to sort all versions in descending order (highest version first).
5. **Output**: Write the sorted versions to `/home/user/project/data/sorted.txt`, one version per line.

The automated verification will run your Python script and check both the correctness of the sort and the execution time. Your script must process the 100,000 items and write the output in under 2.5 seconds.
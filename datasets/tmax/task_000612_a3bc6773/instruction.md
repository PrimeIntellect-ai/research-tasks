You are tasked with building a high-performance C++ tool to organize, merge, and diff massive amounts of project log files. 

You have been provided with a vendored C library at `/app/libfastmerge` which contains highly optimized routines for sorting and merging text buffers. However, the library currently cannot build due to a broken Makefile, and you must integrate it into a new C++ application.

Here is your multi-stage workflow:

1. **Fix the Vendored Library**:
   Navigate to `/app/libfastmerge`. The `Makefile` is broken (it has incorrect compiler flags and fails to create the shared library `libfastmerge.so`). Fix the Makefile, compile the C library, and ensure `libfastmerge.so` is generated successfully.

2. **C++ Implementation**:
   Write a C++ program at `/home/user/organizer.cpp`. 
   Your program must read a list of file-merge requests from a JSON file (provided at `/home/user/requests.json`). Each request contains a `job_id`, `file_A`, and `file_B`.
   
   For each request, your program must:
   - **Validate**: Ensure `file_A` and `file_B` exist and reside within `/home/user/project_files/`. If a path traverses outside this directory (e.g., using `../`), drop the request.
   - **Process**: Read both files into memory and use the C library function `char* merge_buffers(const char* buf1, const char* buf2)` (declared in `/app/libfastmerge/fastmerge.h`) to merge them.
   - **Concurrency**: Process these requests concurrently using C++ threads (`std::thread` or `std::async`). 

3. **Output Format**:
   Your program must write the results to `/home/user/results.jsonl`. Each line must be a valid JSON object with the following schema:
   `{"job_id": <int>, "status": "success|invalid", "merged_length": <int>}`
   - `merged_length` is the string length of the output from `merge_buffers`.

4. **Performance**:
   Your C++ implementation must be highly concurrent. An automated verifier will measure the total execution time of your compiled C++ binary on a dataset of 10,000 merge requests. You must achieve a runtime of less than 2.0 seconds.

**Constraints:**
- Use modern C++ (C++17 or C++20).
- Compile your C++ program to `/home/user/organizer`. Be sure to link against `libfastmerge.so` and configure the `LD_LIBRARY_PATH` or rpath appropriately so it runs.
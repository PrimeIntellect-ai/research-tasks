You are helping a developer organize and optimize their project files. A junior developer recently attempted to port a data integrity tool from Python to C++ because the Python version was too slow for our CI pipeline. 

Unfortunately, the new C++ version (`fast_checksum.cpp`) is failing in CI. While it works occasionally on local machines, it crashes with segmentation faults on certain files, produces incorrect checksums, and consumes excessive memory (memory leaks). This mimics an issue where the test suite passes locally but fails in CI due to undefined behavior and memory safety violations.

Your task:
1. Navigate to `/home/user/project_sync`.
2. Analyze the reference Python implementation (`checksum_ref.py`) to understand the exact custom 16-bit checksum algorithm (Fletcher-16 variant) and the required JSON REST payload format.
3. Fix the memory safety issues (buffer overflows/undefined behavior) and memory leaks in `/home/user/project_sync/fast_checksum.cpp`.
4. Ensure the C++ checksum logic perfectly matches the Python implementation.
5. Update the C++ code so that it processes all files in `/home/user/project_sync/data` in alphabetical order and outputs the results exactly as the Python script does, generating a file at `/home/user/project_sync/api_payload.json`.
6. Compile your fixed C++ program into an executable named `/home/user/project_sync/fast_checksum`. You can use `g++ -std=c++17 fast_checksum.cpp -o fast_checksum`.
7. Run your compiled executable so it generates the `api_payload.json` file.

The final C++ executable must be strictly memory safe. We will run it under `valgrind` in our automated verification to ensure 0 bytes are leaked and there are 0 memory errors.

The final state must contain the cleanly compiled `/home/user/project_sync/fast_checksum` binary and the correct `/home/user/project_sync/api_payload.json`.
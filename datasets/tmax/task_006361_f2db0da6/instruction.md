I am working on a simple C++ CGI executable that acts as a REST API endpoint to organize and list project files. The source code is located at `/home/user/file_api.cpp`. It reads the `QUERY_STRING` environment variable (expecting a format like `dir=/some/path`), recursively scans that directory, and outputs an HTTP JSON response containing the file tree and file sizes.

However, the current implementation has several memory safety issues, undefined behaviors, and memory leaks. It often crashes with segmentation faults on deep directories or long file names.

Your tasks are:
1. Debug and fix the memory safety issues and undefined behaviors in `/home/user/file_api.cpp` without changing its core logic or the output JSON structure. Ensure there are no buffer overflows and no memory leaks.
2. Compile the fixed code to `/home/user/file_api` using `g++ -O2 -Wall /home/user/file_api.cpp -o /home/user/file_api`.
3. Create a property-based testing script at `/home/user/test_api.sh` (and make it executable). This script should:
   - Generate 10 random directory structures under `/home/user/test_run_X` (where X is 1 to 10). Each should contain a random mix of files (with random names and sizes) and subdirectories up to 3 levels deep. Ensure some filenames and paths are exceptionally long to test buffer limits.
   - For each generated directory, run the CGI executable by setting `QUERY_STRING="dir=/home/user/test_run_X"`.
   - Capture the stdout of the executable.
   - Verify that the output strictly begins with `Content-Type: application/json\r\n\r\n` (followed by the JSON body).
   - Strip the HTTP headers and verify that the remaining body is valid JSON using `jq`.
   - Verify that the executable exits with a status code of 0.
   - If any test fails or crashes, the script must print an error and exit with a non-zero status. If all 10 tests pass, it should print a success message and exit with 0.

Ensure your compiled `/home/user/file_api` runs flawlessly on valid directories without memory errors. You can use Valgrind or AddressSanitizer during your debugging process to ensure memory safety.
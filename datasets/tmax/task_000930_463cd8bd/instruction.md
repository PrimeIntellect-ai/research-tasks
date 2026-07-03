You are an engineer tasked with porting a legacy mathematical sequence tool into a minimal container environment. The tool parses pseudo-URLs, extracts numerical sequences, and performs mathematical sorting and merging. 

The source code is located in `/home/user/math_port`. It consists of:
- `mathops.h` and `mathops.c`: Contains mathematical operations.
- `router.c`: A command-line wrapper that simulates HTTP URL routing and parameter parsing for mathematical operations.

To complete this porting task, you must:

1. **Fix Memory Leaks**: The current implementation of `router.c` has memory leaks when parsing the URL parameters and allocating arrays. Find and fix these memory leaks so that the program runs perfectly clean under Valgrind.
2. **Shared Library Management**: Compile `mathops.c` into a shared library named `libmathops.so` in `/home/user/math_port`.
3. **Conditional Build**: Compile `router.c` into an executable named `math_router` in `/home/user/math_port`. You must link it dynamically against `libmathops.so`. Additionally, you must compile `router.c` with the C preprocessor macro `MINIMAL_CONTAINER=1`. This macro changes the output format of the router to a strict JSON format required by the new container API. 
4. **Execution and Verification**:
   - Run your compiled executable using Valgrind to ensure there are no memory leaks. Use exactly this command format (ensure `LD_LIBRARY_PATH` is set appropriately):
     `valgrind --leak-check=full --error-exitcode=1 ./math_router "/math/merge?seq1=42,15,8&seq2=4,16,23"`
   - If the leak is correctly fixed, it will exit with code 0.
   - Save the standard output of the successful execution of `./math_router "/math/merge?seq1=42,15,8&seq2=4,16,23"` (without valgrind output) to `/home/user/container_out.json`.
5. **Diffing**: The legacy system expected the result sequence to include the number `1` at the beginning. The file `/home/user/expected_legacy.json` contains this old expectation. Run a unified diff (`diff -u`) comparing `/home/user/expected_legacy.json` to your new output `/home/user/container_out.json` and save the diff output to `/home/user/api_diff.txt`.

Ensure all requested files (`libmathops.so`, `math_router`, `container_out.json`, `api_diff.txt`) are placed exactly at the specified paths.
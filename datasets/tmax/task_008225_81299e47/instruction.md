You are an engineer tasked with preparing a minimal C-based TCP logging service (`minilogd`) to run safely inside a constrained container environment. The current codebase has several issues preventing it from compiling, running reliably, and passing automated deployment checks.

Your workspace is located at `/home/user/minilogd_project`. 

You need to accomplish the following objectives:

1. **Fix the Build Failure (Circular Dependency):** 
   The code currently fails to compile due to a circular dependency between `protocol.h` and `types.h`. Refactor the headers (e.g., using forward declarations or reorganizing definitions) so that `make` successfully builds the `minilogd` executable. Do not change the function signatures.

2. **Memory Debugging and Profiling:**
   The application contains a memory leak and a buffer overflow in the `process_client_message` function located in `server.c`. Use Valgrind (or your preferred memory debugger) to identify and fix these memory issues. The service must run under Valgrind with zero memory leaks and zero invalid read/writes.

3. **Unit and Integration Testing:**
   Write a unit test file named `test_protocol.c` in the project directory. It should compile into a `test_protocol` executable when `make test` is run (you will need to update the Makefile). The test should verify that the `parse_message` function correctly extracts the payload from a formatted string (e.g., "MSG:Hello" -> "Hello"). The test executable must exit with code 0 on success.

4. **End-to-End Test Orchestration:**
   Create an orchestration script at `/home/user/minilogd_project/run_e2e.sh`. The script must:
   - Build the project (`make clean all test`).
   - Run the unit tests.
   - Start the `minilogd` server in the background on port `8080`, wrapped in Valgrind (e.g., `valgrind --leak-check=full --error-exitcode=1 ./minilogd 8080`).
   - Use `nc` (netcat) or `/dev/tcp` to send the string `"MSG:E2E_TEST_PAYLOAD\n"` to `127.0.0.1:8080`.
   - Send the string `"QUIT\n"` to shut down the server gracefully.
   - Wait for the server process to exit.
   - If all steps succeed, the script must write the exact string `E2E_STATUS: SUCCESS` to `/home/user/e2e_report.txt`. If any step fails (including valgrind detecting a leak), it should write `E2E_STATUS: FAILED`.

Make sure the `run_e2e.sh` script is executable. You have all necessary tools (gcc, make, valgrind, netcat) installed in the environment.
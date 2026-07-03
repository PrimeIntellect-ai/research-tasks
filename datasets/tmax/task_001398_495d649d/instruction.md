You are a systems programmer taking over a legacy mathematical analysis service written in C. The service exposes a TCP socket server that performs intensive mathematical calculations (like prime factorization). 

Your goal is to apply a new feature patch, fix several build/linking issues, implement missing request validation, and verify the service works.

The project is located at `/home/user/math_service/`.

Here are your instructions:
1. **Apply the Patch**: Apply the patch file located at `/home/user/math_service/feature.patch`. This patch introduces a new advanced factoring algorithm but is currently unapplied.
2. **Conditional Compilation & Build System**: 
   - The original `Makefile` is broken. It fails to properly build the shared library `libmathcore.so` and fails to link it to the main `math_server` executable.
   - Fix the `Makefile` so that `libmathcore.so` is compiled as a shared library (it currently lacks position-independent code flags).
   - Ensure `math_server` is linked against `libmathcore.so`. Make sure the executable can find the shared library at runtime without relying on a globally set `LD_LIBRARY_PATH` (e.g., configure the rpath to the current directory `$ORIGIN` or the specific path `/home/user/math_service`).
   - The new feature in the patch is wrapped in a preprocessor directive. You must modify the `Makefile` to compile the project with the `ENABLE_ADV_MATH` macro defined so the new code is included.
3. **Request Validation**: 
   - Inspect `server.c`. The server reads an integer from incoming TCP connections and processes it.
   - The new patched code requires that inputs be strictly positive. Modify `server.c` to add request validation: immediately after parsing the integer `n` from the client, if `n < 0`, the server must send the exact string `"ERR_NEGATIVE\n"` to the client and close the connection, skipping any mathematical processing.
4. **Compile and Run**:
   - Compile the project successfully by running `make`.
   - Start the server in the background. It listens on port `8080`.
5. **Generate Verification Log**:
   - Connect to the server on `127.0.0.1:8080` and send the string `"-42\n"`. Capture the response.
   - Connect again and send the string `"15\n"`. Capture the response.
   - Write the responses (exactly as received) to `/home/user/math_service/test_results.log`, one per line.

Ensure the final server binary `/home/user/math_service/math_server` and library `/home/user/math_service/libmathcore.so` are built and left on the disk, and the server process is left running.
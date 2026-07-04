You have inherited an unfamiliar, legacy codebase for a custom HTTP-based telemetry server. The source code is located in `/home/user/telemetryd`. Unfortunately, the previous developer left it in a broken state. Your goal is to fix the build, extract the lost configuration parameters, debug a runtime crash, and finally leave the server running so it can be tested.

Here are your objectives:

1. **Fix the Build (Compiler/Linker Errors):**
   Navigate to `/home/user/telemetryd` and run `make`. The build currently fails due to a linker error. Diagnose and fix the `Makefile` or source files so that the `telemetryd` executable builds successfully.

2. **Recover Configuration:**
   The server requires a configuration file at `/home/user/telemetryd/config.ini` specifying the `PORT` and `AUTH_TOKEN`. These values were lost, but the previous developer left a scanned note at `/app/server_notes.png`. You must inspect this image (e.g., using `tesseract`) to recover the port number and the authentication token. Create the `config.ini` file with the following format:
   ```ini
   PORT=<recovered_port>
   AUTH_TOKEN=<recovered_token>
   ```

3. **Debug the Runtime Crash (Memory/Debugger usage):**
   Once built and configured, start the server. You will notice that it immediately segfaults when it receives its first valid HTTP request. Use an interactive debugger (like `gdb`) to inspect the memory and stack trace, identify the root cause of the crash (e.g., a null pointer dereference or buffer overflow in the request parser), and patch the C/C++ source code. Recompile the server.

4. **Construct a Regression Test:**
   Write a bash script at `/home/user/telemetryd/test_regression.sh` that sends an HTTP GET request to `http://127.0.0.1:<PORT>/health` with the header `Authorization: Bearer <AUTH_TOKEN>`. The script should exit with code 0 if the server responds with HTTP 200 OK, and exit with code 1 otherwise.

5. **Final State:**
   Leave the fixed `telemetryd` server running in the background. The automated verifier will issue real HTTP requests to the port recovered from the image to verify the server is stable, processes the auth token correctly, and does not crash.
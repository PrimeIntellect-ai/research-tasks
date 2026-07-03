You are an engineer tasked with fixing and completing a polyglot mathematical computation server. The project is located in `/home/user/math_server`. It consists of a high-performance C extension for calculating the number of steps in the Collatz conjecture, wrapped in a Python WebSocket server. 

Currently, the project is broken: the build system configuration (`setup.py`) is flawed, the C code contains a compilation/logic error under conditional compilation, and the Python server lacks proper request validation.

Your tasks are to:

1. **Fix the Polyglot Build System (`setup.py`)**:
   - The `setup.py` file is heavily broken. Fix it so that it correctly compiles the C extension (`src/fastmath.c`).
   - Implement conditional compilation: if the environment variable `ENABLE_OPT=1` is set during build, the build system must pass the `-DUSE_OPTIMIZED` macro to the C compiler.
   - Ensure the package defines its dependencies correctly (it requires the `websockets` Python package).

2. **Fix the C Extension (`src/fastmath.c`)**:
   - The C function `collatz_steps` has a bug in the `#ifdef USE_OPTIMIZED` block. Fix the logic so it correctly calculates the Collatz steps. (Remember: if $n$ is even, $n = n/2$; if $n$ is odd, $n = 3n + 1$. Stop when $n = 1$).

3. **Implement Request Validation (`server.py`)**:
   - Modify the WebSocket server to validate incoming requests.
   - The server expects integer strings. Validate that the input is a positive integer strictly between `1` and `1000000` (inclusive).
   - If the input is invalid, the server must reply with the exact string `"ERROR: Invalid input"`.

4. **Build and Test**:
   - Build and install the package into the current environment using `ENABLE_OPT=1 pip install .`.
   - Start the server (`python3 server.py &`) on port `8765`.
   - Write a bash script `/home/user/test_client.sh` that sends three messages to the WebSocket server: `15`, `2000000`, and `27`. 
   - The script must save the server's responses, one per line, into `/home/user/test_results.log`.

**Constraints & Verification**:
- The C source files are in `/home/user/math_server/src/`.
- The python server script is `/home/user/math_server/server.py`.
- Do not use any external dependencies other than `websockets` for the server. You can use any CLI tools (like `curl`, `wscat`, or a python script) in `test_client.sh` to query the server.
- We will verify the contents of `/home/user/test_results.log` and the installed package.
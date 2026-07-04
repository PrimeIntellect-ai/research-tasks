You are helping migrate a data processing pipeline from Python 2 to Python 3. The pipeline reads mathematical expressions, sends them over a WebSocket to an evaluation server, and records the results.

You need to complete the pipeline by performing the following steps:

1. **Patch the Client:**
   There is a Python 2 script at `/home/user/client.py` and a patch file at `/home/user/upgrade.patch`. Apply the patch to `client.py` to make it Python 3 compatible. It uses the `websockets` and `asyncio` libraries.

2. **Write the C Evaluator:**
   The core evaluation logic must be written in C. Create a file `/home/user/evaluator.c` that implements a prefix notation (Polish notation) expression parser. 
   - It must export a function: `int evaluate_prefix(const char* expr)`
   - The parser should support integer arithmetic with operators `+`, `-`, `*`, and `/`.
   - Operands and operators will be space-separated (e.g., `+ 3 * 4 5` evaluates to 23).
   - Compile this C code into a shared library at `/home/user/evaluator.so` (use `gcc -shared -o evaluator.so -fPIC evaluator.c`).

3. **Create the WebSocket Server:**
   Write a Python 3 script `/home/user/server.py` that acts as a WebSocket server on `ws://localhost:8080`.
   - Use the `websockets` library.
   - For every text message received, pass the string to the `evaluate_prefix` function in `evaluator.so` using the `ctypes` module.
   - Send the integer result back as a string over the WebSocket.

4. **Run and Verify:**
   Start your server in the background. Then, execute the patched `client.py`. 
   The client will read expressions from `/home/user/equations.txt`, send them to your server, and write the answers line-by-line to `/home/user/output.txt`.

Ensure all operations are completed in `/home/user`.
You are an integration developer responsible for testing and securing a backend mathematical evaluation API. The API is a Python-based WebSocket server located at `/home/user/math_api.py` that listens on `ws://localhost:8080`.

Currently, the server has three major issues:
1. **Security Vulnerability:** It uses Python's unsafe `eval()` to calculate mathematical expressions.
2. **Memory Leak:** It indefinitely stores every received message in a global `history` list, causing unbounded memory growth.
3. **No Integration Tests:** There is no client to automate testing of the expressions over WebSockets.

Your task is to fix these issues and profile the fixed server:

**Phase 1: Fix the Server (`/home/user/math_api.py`)**
1. Replace `eval()` with a safe, custom expression parser using Python's `ast` module. The parser must evaluate strings containing numbers and the basic arithmetic operators (`+`, `-`, `*`, `/`). It should reject any other operations or functions (returning `"ERROR"`).
2. Fix the memory leak by ensuring the global `history` list never exceeds exactly 10 items. Older items should be discarded.
3. Keep the logic where sending the exact string `"SHUTDOWN"` causes the WebSocket server to gracefully exit the event loop.

**Phase 2: Write the Test Client (`/home/user/test_client.py`)**
Write a Python WebSocket client that:
1. Connects to `ws://localhost:8080`.
2. Sends the following sequence of mathematical expressions one by one (waiting for the response before sending the next):
   - `"15 + 27"`
   - `"100 / 4"`
   - `"8 * 9"`
   - `"50 - 14"`
   - `"__import__('os').system('echo hacked')"`
3. Collects the server's responses and writes them to `/home/user/test_output.json` as a JSON array of values (e.g., `[42, 25.0, ...]`). The last item should evaluate to `"ERROR"` because of your safe AST parser.
4. Sends the `"SHUTDOWN"` command to gracefully terminate the server and then closes the client connection.

**Phase 3: Execution and Profiling**
1. Install any necessary dependencies (`websockets`, `memory_profiler`).
2. Run the modified server using `memory_profiler`'s `mprof` tool. Output the profile data to `/home/user/mprof.dat`. Run: `mprof run --output /home/user/mprof.dat python /home/user/math_api.py` (run this in the background).
3. Run your client (`python /home/user/test_client.py`) to execute the integration test and trigger the shutdown.

Ensure the final state contains:
- The secured and leak-fixed `/home/user/math_api.py`.
- The test client `/home/user/test_client.py`.
- The exact output file `/home/user/test_output.json`.
- The memory profile file `/home/user/mprof.dat`.
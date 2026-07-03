You are a systems programmer investigating a build and test failure in a Python project. The test suite passes on some developers' machines but fails consistently in CI due to dynamic linking and import ordering issues.

The project relies on four interconnected C libraries that process data. You need to write a builder and a test runner that correctly resolves dependencies, compiles the C code, and imports the libraries in the exact correct order.

Here is your environment and requirements:
1. Workspace: `/home/user/workspace`
2. C Source Files: Located in `/home/user/workspace/src/`. You will find `modA.c`, `modB.c`, `modC.c`, and `modD.c`.
3. Dependency Server: A local WebSocket server is available. You must first start it by running `python3 /home/user/workspace/ws_server.py &`. It listens on `ws://localhost:8765`. When connected, it immediately sends a JSON object representing the dependency graph of the modules (e.g., `"modB": ["modA"]` means `modB` depends on `modA`).
4. You must write a Python script `/home/user/workspace/builder.py` that:
   - Connects to `ws://localhost:8765` using the `websockets` library.
   - Receives the JSON dependency graph.
   - Performs a topological sort on the graph to determine the correct build and load order.
   - Compiles the four C files into shared libraries (`.so`) in the root workspace directory (`/home/user/workspace/`). You should use `gcc -shared -fPIC` to compile them. Do not explicitly link them to each other (do not use `-l`).
5. You must write a Python script `/home/user/workspace/run_test.py` that:
   - Uses `ctypes` to load the compiled `.so` libraries in the exact topological order you computed.
   - Because the libraries rely on symbols from their dependencies and are not explicitly linked, you MUST load them using the `ctypes.RTLD_GLOBAL` mode to simulate fixing the "import ordering CI issue". If you load them in the wrong order or without `RTLD_GLOBAL`, the OS dynamic linker will throw an undefined symbol error.
   - Calls the `getD()` function from `modD.so`.
   - Writes the integer result returned by `getD()` to `/home/user/workspace/result.txt`.

Constraints:
- You may use `pip install websockets` if it is not already installed.
- Do not modify the provided C files.
- You must create both `builder.py` and `run_test.py` and ensure `/home/user/workspace/result.txt` is created with the correct final answer.
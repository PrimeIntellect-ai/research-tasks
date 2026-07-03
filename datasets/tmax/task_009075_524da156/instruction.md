You are an AI assistant helping a script developer create and debug some mathematical utilities. 

We have a C library that implements a numerical algorithm (Newton-Raphson method for square roots) and a Python WebSocket server that serves this algorithm. However, the project is currently broken in multiple ways:

1. **Buggy Math Implementation:** The C source file at `/home/user/math_utils/mathops.c` has a mathematical error in the algorithm. A colleague has provided a patch file at `/home/user/math_utils/fix_math.patch`. You need to apply this patch to fix the logic.
2. **Linker Error:** The project uses CMake (`/home/user/math_utils/CMakeLists.txt`) to build a shared library (`libmathops.so`). However, it currently fails to compile/link properly because it cannot find the standard math library (`libm`) at link time. You need to modify the `CMakeLists.txt` so it successfully links the math library.
3. **Build the Library:** Build the shared library inside the `/home/user/math_utils/build/` directory.
4. **Run the WebSocket Server:** A pre-written Python WebSocket server exists at `/home/user/ws_server.py`. It relies on the built `libmathops.so`. Run this server in the background. It will listen on `ws://localhost:8765`.
5. **WebSocket Communication:** Write a small script (e.g., in Python) or use a CLI tool to connect to `ws://localhost:8765`. Send the number `612.0` as a string to the server. 
6. **Save the Result:** The server will reply with the computed square root. Save the exact string received from the server into a file at `/home/user/result.txt`.

Ensure your final step creates the `/home/user/result.txt` file containing only the computed numerical result. All necessary dependencies (like `cmake`, `make`, `gcc`, and Python's `websockets` package) are available or can be installed via standard package managers.
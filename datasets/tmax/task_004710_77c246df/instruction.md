You are an engineer working on porting a legacy numerical tool to run as a microservice in a minimal container environment. 

We have a small C project located in `/home/user/project/` that calculates the square root of a number using the Newton-Raphson method. Currently, it compiles to a standalone executable, but we need it to be a shared library that can be consumed by a modern Python service over WebSockets.

Your tasks are:

1. **Fix the Makefile**: 
   Modify `/home/user/project/Makefile` so that running `make` (inside `/home/user/project/`) compiles `algo.c` into a shared library named `libalgo.so`. You must ensure the C code is compiled as Position Independent Code (PIC) and properly linked as a shared object. The `compute_root` function must be exported and usable.

2. **Create a Python WebSocket Server**:
   Write a Python script at `/home/user/project/ws_server.py` that implements a WebSocket server using the standard `websockets` library (which is already installed) and `asyncio`.
   - The server must listen on `localhost` port `8765`.
   - Use the `ctypes` library to load `/home/user/project/libalgo.so`.
   - The server must accept incoming text messages containing a single floating-point number (e.g., `"16.0"`).
   - For each received message, parse it as a float, pass it to the C function `double compute_root(double)`, and send the resulting double back to the WebSocket client as a string.
   - When the server successfully starts and is listening, it should write the exact string `SERVER READY` to a file at `/home/user/project/server_ready.log` before starting its main event loop.

Note: 
- Do **not** leave the server running in the foreground blocking the terminal when you are done. Just write the code, compile the library using `make`, and ensure the scripts are ready. Our automated tests will launch `ws_server.py` and verify its behavior.
- Ensure the ABI definitions in `ctypes` correctly specify `c_double` for both the argument types (`argtypes`) and the return type (`restype`) of the `compute_root` function.
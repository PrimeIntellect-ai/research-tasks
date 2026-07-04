You are a systems programmer tasked with fixing a broken polyglot project. 

In `/home/user/project`, there is a C library (`libencoder`), a C++ wrapper (`wrapper.cpp`), and a Makefile. The C library takes a string and converts it to a custom hex string representation (handling basic character encoding). 

However, the project is currently broken in multiple ways:
1. **Linking Issue:** Running `make` fails to build `libencoder.so` and `wrapper.so` properly. There are compilation/linking errors and missing compiler flags. Also, the C++ wrapper fails to resolve symbols from the C library due to name mangling (missing `extern "C"`).
2. **Memory Safety Issue:** The C code `libencoder.c` contains undefined behavior and memory safety bugs (e.g., off-by-one error or missing null terminators for strings) that cause segfaults when called.
3. **Missing Component:** The project is supposed to expose this functionality over a WebSocket. 

Your tasks:
1. Fix the Makefile, `libencoder.h`, and `libencoder.c` so that running `make` in `/home/user/project` cleanly builds `libencoder.so` and `wrapper.so` without errors.
2. Fix the memory safety bug in `libencoder.c` so it doesn't crash.
3. Create a Python script `/home/user/project/ws_server.py` that starts a WebSocket server on `ws://localhost:8765`. 
   - Use the `websockets` Python library (it is installed).
   - Use `ctypes` to load `wrapper.so` and call its `encode_string(const char*)` function.
   - When the server receives a text message, it should pass it to `encode_string`, and send the resulting hex string back over the WebSocket. Ensure you properly free the returned string if necessary, or just rely on the wrapper's memory handling. (The wrapper's `encode_string` returns a newly allocated string that should ideally be freed, but memory leaks in the Python wrapper won't be strictly tested. The segfault in the C library *will* be tested).
4. Run your server in the background and verify it works.

To prove it works, write a client script or use a tool to send the exact string `"PolyglotData123"` to your WebSocket server. Save the server's response (the encoded hex string) to `/home/user/output.log`.
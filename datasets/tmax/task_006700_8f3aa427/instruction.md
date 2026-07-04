You are a build engineer responsible for artifact verification. We need to deploy a microservice that checks if an artifact manifest satisfies a set of dependency constraints. 

You have been provided with the source code for the constraint solver and a simple HTTP stub in `/home/user/workspace/`.

Here is what you need to do:

1. **Shared Library Management:**
   - Compile `solver.cpp` into a dynamic shared library named `libsolver.so`.
   - Ensure the library is compiled with position-independent code.

2. **REST API Service Construction:**
   - Write a C++ program named `server.cpp` in the same directory.
   - Use the provided `http_stub.h` to start an HTTP server on port `8123`.
   - Implement the `handle_post` callback. The server will receive a POST request to `/verify` with a plain text body in this exact format:
     ```
     EXPR: <comma-separated constraints>
     MANIFEST: <comma-separated key:value pairs>
     ```
     Example body:
     ```
     EXPR: libA>=2,libB==1
     MANIFEST: libA:3,libB:1
     ```
   - Parse this body, and pass the `EXPR` string and `MANIFEST` string to the `evaluate_constraints(const char* expr, const char* manifest)` function defined in `solver.h`.
   - If `evaluate_constraints` returns `true`, respond with HTTP status 200 and body `{"status": "pass"}`.
   - If it returns `false`, respond with HTTP status 400 and body `{"status": "fail"}`.

3. **Build System:**
   - Write a `Makefile` in `/home/user/workspace/` that has at least the following targets:
     - `libsolver.so`: builds the shared library.
     - `server`: builds the `server` executable from `server.cpp`, dynamically linking against `libsolver.so`.
     - `all`: builds both.

4. **Execution:**
   - Build the project using your `Makefile`.
   - Start the server in the background so it listens on port 8123.
   - Ensure the server can find `libsolver.so` at runtime.
   - Write the running server's PID to `/home/user/workspace/server.pid`.
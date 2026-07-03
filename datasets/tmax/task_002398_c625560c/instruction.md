You are an open-source maintainer reviewing a pull request for a legacy microservice. The service receives binary data over HTTP, computes a custom cryptographic fingerprint (combining a CRC32 checksum and a numerical polynomial evaluation), and returns the result. 

Currently, the service runs on a slow Python script. A contributor has submitted a PR to rewrite the core logic and the HTTP server in C++ for performance. However, the PR is broken in multiple ways:

1. **Vendored Dependency Issue:** The project builds against a vendored copy of `zlib` located at `/app/vendored/zlib-1.3.1`. The contributor accidentally introduced a typo in the vendored library's `Makefile`, causing compilation to fail.
2. **Translation Bugs:** The C++ implementation of the fingerprint algorithm in `/app/src/fingerprint.cpp` has subtle bugs. It does not perfectly match the output of the reference Python implementation provided in `/app/legacy/reference.py`. You will need to analyze the Python code, identify the translation errors (likely involving data types, overflows, or sign extensions), and fix the C++ code.
3. **Integration:** The C++ server code in `/app/src/server.cpp` needs to be linked against the fixed vendored `zlib`, compiled, and executed.

**Your Objectives:**
1. Fix the build configuration for the vendored package at `/app/vendored/zlib-1.3.1` so it can be compiled successfully (e.g., producing `libz.a`).
2. Debug and fix the numerical and checksum logic in `/app/src/fingerprint.cpp` so its output strictly matches `reference.py` for any given byte sequence.
3. Compile the C++ HTTP server. You can write your own build script or compile command, ensuring it links against your newly compiled `libz.a`.
4. Start the compiled C++ service. It must listen for HTTP POST requests on `127.0.0.1:9090` at the `/compute` endpoint.

**Protocol Details:**
- The server must listen on `127.0.0.1:9090`.
- It must accept `POST /compute` requests with raw binary bodies.
- It must respond with an `HTTP/1.1 200 OK` containing exactly the fingerprint string computed by the algorithm (format: `XXXXXXXX-YYYYYYYY`, where X is the zero-padded hex CRC32, and Y is the zero-padded hex polynomial evaluation), followed by a newline.

Leave the server running in the background when you are finished so the verification test suite can issue real HTTP requests to it.
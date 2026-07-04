I have a polyglot system composed of a C++ shared library and a Go API server, located at `/home/user/workspace`. However, the build is currently broken due to linking issues, and the Go server implementation is incomplete.

Your task is to fix the build, complete the implementation, and bring up the server.

Here are your instructions:

1. **Extract Configuration from Image**:
   There is an architectural diagram at `/app/spec.png`. Use OCR (e.g., `tesseract`) to read the text from this image. It contains two critical pieces of configuration:
   - A port number (labeled `PORT:`)
   - An authentication token (labeled `AUTH_TOKEN:`)

2. **Fix the C++ Library Compilation and Linking**:
   The C++ code is in `/home/user/workspace/cpp`. It builds a shared library `libprocessor.so` using CMake. However, the Go code fails to link to it because the C++ header and source don't correctly export the functions for C-linkage, and the Go code's `cgo` directives are missing the correct library paths.
   - Fix the C++ source and headers so they can be called from C/Go.
   - Fix the `cgo` directives in the Go code to properly link against the compiled `libprocessor.so`.

3. **Implement Go Concurrency**:
   In `/home/user/workspace/go/server.go`, complete the `/process` HTTP endpoint. It will receive a JSON POST payload like `{"data": [5, 1, 9, 2]}`. 
   - You must split the input array into two halves.
   - Process both halves concurrently using goroutines and channels, calling the C++ `process_array` function via `cgo` for each half.
   - Recombine the processed arrays, sort the entire array in ascending order (using Go's `sort` package), and return it as JSON: `{"result": [...]}`.

4. **Service Configuration**:
   - The Go HTTP server must listen on the `0.0.0.0` address on the exact port extracted from the image.
   - The `/process` endpoint must require an `Authorization` header in the format `Bearer <AUTH_TOKEN>`, using the token extracted from the image. If missing or incorrect, return HTTP 401.
   
5. **Start the Service**:
   Compile the C++ library, build the Go server, and leave the server running in the background. Make sure the shared library is discoverable at runtime (e.g., using `LD_LIBRARY_PATH`).

Make sure the service is actively listening before you finish!
You are tasked with implementing a C++ Web Application Firewall (WAF) to detect and block malicious character encoding bypasses, using a vendored HTTP library. You will also need to write a concurrent Go-based stress tester to verify its stability.

Here is the setup:
1. We have vendored `cpp-httplib` (v0.14.1) at `/app/vendored/cpp-httplib`. However, an intern accidentally broke its `Makefile` and inserted a compilation error in `httplib.h` (around line 100, the `httplib::Server` class name was mangled). You must fix the vendored package so it can be used.
2. In `/app/server`, write a C++ HTTP server (`waf_server.cpp`) using the fixed `cpp-httplib`. It must listen on `127.0.0.1:8080`.
3. The server must implement a security filter translated from a provided Go reference implementation located at `/app/reference/waf.go`. This Go code contains logic to decode multiple layers of URL and Unicode hex encoding, looking for directory traversal attempts (e.g., `../` or `%c0%af`). Translate this precise decoding and detection logic into C++. 
4. The C++ server should respond to `GET` requests on any path. If the WAF logic detects a traversal attempt in the decoded URI, it must respond with HTTP status `403 Forbidden` and the body `Blocked`. Otherwise, it must respond with HTTP status `200 OK` and the body `OK`.
5. In `/app/tester`, write a Go program (`tester.go`) that utilizes Go concurrency patterns (goroutines and channels) to send 100 concurrent HTTP GET requests to `http://127.0.0.1:8080/valid_path`. It should collect the HTTP status codes and print `Success` if all responses are 200. Run this tester to ensure your C++ server handles concurrent connections without crashing.
6. Leave your C++ server running in the background listening on `127.0.0.1:8080` before finishing the task.

Build your C++ server statically or ensure it dynamically links correctly in the environment, outputting the binary to `/app/server/waf_server`.
You are an engineer tasked with preparing a custom Web Application Firewall (WAF) reverse proxy for deployment in a minimal Linux container. 

The proxy is written in Go and uses a legacy C library via Cgo to sanitize HTTP headers. Recently, the proxy has been crashing when receiving unusually large HTTP headers. Your investigation suggests a memory safety issue (buffer overflow) in the C library.

The codebase is located in `/home/user/waf-proxy`.

Your tasks:
1. **Fix the Memory Leak / Buffer Overflow:** Analyze and fix `/home/user/waf-proxy/sanitizer.c`. The `sanitize_header` function must safely truncate the input string if it exceeds `max_len - 1`, ensuring the output is always properly null-terminated and no out-of-bounds writes occur.
2. **Compile a Statically Linked Binary:** Write a bash script `/home/user/waf-proxy/build.sh` that compiles the Go application into a fully statically linked executable named `static-waf` in the same directory. The resulting binary must not have any dynamic dependencies (e.g., it should report "not a dynamic executable" when checked with `ldd`). 
3. **Run Script:** Create a script `/home/user/waf-proxy/run.sh` that starts the `static-waf` binary in the background and writes its PID to `/home/user/waf-proxy/proxy.pid`.

**Application Details:**
- The Go reverse proxy listens on `127.0.0.1:8080`.
- It forwards traffic to a backend at `127.0.0.1:9090`.
- It uses the C function `void sanitize_header(const char* input, char* output, int max_len);` to process the `X-Custom-User` header. The Go code passes a pre-allocated buffer of 64 bytes (`max_len = 64`).

Ensure your `build.sh` script installs any necessary alpine/debian packages (e.g., `musl-tools`, `musl-dev`) locally if needed to achieve a static Cgo build, though standard `gcc` static compilation flags may suffice if the system has static libc available.
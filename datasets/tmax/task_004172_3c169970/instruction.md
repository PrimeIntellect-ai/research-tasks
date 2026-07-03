You are a developer tasked with fixing and securing a multi-file custom C-based reverse proxy that sits in front of a Go-based REST API.

Currently, the project is in a broken state. The C proxy fails to compile, the Go backend has a concurrency issue, and the API needs a Web Application Firewall (WAF) filter to block malicious requests. 

Your objectives are:

1. **Fix the Go Backend:**
   In `/app/backend/`, there is a simple Go REST API (`main.go`) that uses goroutines to process requests. It currently has a race condition or compilation error. Fix the Go code so it compiles and runs reliably on `127.0.0.1:8080`.

2. **Fix the C Reverse Proxy Compilation:**
   In `/app/proxy/`, the C source code for the reverse proxy (`main.c`, `filter.c`, `filter.h`, `proxy.c`) fails to compile due to syntax errors and missing includes. Fix these compilation errors.

3. **Audio Extraction for Authentication:**
   There is an audio file located at `/app/auth_token.wav`. It contains a single spoken English word. You must extract/transcribe this word. The C reverse proxy must be modified to inject an HTTP header `X-Proxy-Auth: <transcribed_word>` into every request it forwards to the Go backend.

4. **Implement the Adversarial Filter:**
   The file `/app/proxy/filter.c` contains an empty function `int validate_payload(const char* payload)`. You must implement this function to act as a WAF. 
   - It must return `0` if the payload is benign.
   - It must return `1` if the payload contains malicious patterns (e.g., SQL injection, Command Injection, XSS).
   To help you develop this, we have provided two directories of raw HTTP POST body payloads:
   - `/app/corpus/clean/` (contains files with benign JSON data)
   - `/app/corpus/evil/` (contains files with malicious data)
   Your implementation in `filter.c` must correctly classify 100% of the payloads in both directories.

5. **Deployment:**
   Create a bash script at `/app/build_and_run.sh` that compiles the C proxy into an executable named `c-proxy` (using `gcc`), starts the Go backend in the background, and then starts the C proxy on `127.0.0.1:8000`.

Ensure your C code is robust and your filter correctly handles all cases in the provided corpora. Do not change the function signature of `validate_payload`.
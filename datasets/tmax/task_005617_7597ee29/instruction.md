You are a web developer tasked with building a lightweight Web Application Firewall (WAF) feature for a custom Go-based reverse proxy. The proxy needs to inspect incoming HTTP request URIs for SQL injection attempts before forwarding them to a backend server. 

For performance reasons, the actual detection logic must be written in C using a custom state machine, which will be called from Go using `cgo`.

Your objectives are to implement the C library, the Go reverse proxy, and then start the proxy. Finally, verify its operation.

### Step 1: Implement the C State Machine WAF
Create a C header and source file at `/home/user/waf/waf.h` and `/home/user/waf/waf.c`.
The C code must expose a function: `int detect_sqli(const char *input);`
This function must use a manual character-by-character **state machine** (do not use regex or standard string library search functions like `strstr`) to detect the specific sequence of words: `UNION` followed by `SELECT`, separated by one or more space characters (` `).
- The detection must be **case-insensitive**.
- It should match patterns like `union select`, `UnIoN    SeLeCt`, `UNION SELECT`.
- It must return `1` if the pattern is detected anywhere in the input string, and `0` otherwise.

### Step 2: Implement the Go Reverse Proxy
Create a Go application at `/home/user/waf/proxy.go`.
- The proxy must listen on port `8080` (`127.0.0.1:8080`).
- It must act as a reverse proxy, forwarding all requests to a backend server located at `http://127.0.0.1:9090`.
- Before forwarding, it must extract the full request URI (path + query string) and pass it to the C function `detect_sqli` via `cgo`.
- If the C function returns `1` (SQLi detected), the proxy MUST NOT forward the request. Instead, it must immediately respond with an HTTP `403 Forbidden` status code and the exact plain text body `Blocked by WAF\n`.
- If the C function returns `0` (Safe), the proxy must forward the request to the backend server and return the backend's response to the client.

### Step 3: Build and Run
Build the Go application.
Start a dummy backend server on port `9090` (e.g., using `python3 -m http.server 9090 --bind 127.0.0.1` in the background).
Run your Go reverse proxy in the background.

### Step 4: Verification Logging
Create a bash script at `/home/user/test_waf.sh` that uses `curl` to test the proxy and writes the HTTP status codes to `/home/user/waf_test.log`. 
The script should test the following URLs in order, outputting only the HTTP status code (e.g., using `curl -s -o /dev/null -w "%{http_code}\n" <url>`) to the log file, one code per line:
1. `http://127.0.0.1:8080/products?search=apple`
2. `http://127.0.0.1:8080/items?q=UnIoN%20%20%20sElEcT%20*`
3. `http://127.0.0.1:8080/union_and_select` (Safe, because there is no space between them, just underscores)
4. `http://127.0.0.1:8080/?test=union+select` (Note: in raw URI, `+` is just a plus character. Our state machine expects a space ` `, but standard HTTP clients send spaces encoded as `%20`. Wait, `curl` sends exactly what you type. Test exactly: `http://127.0.0.1:8080/?test=union%20select`)

Run the script so `/home/user/waf_test.log` is generated.
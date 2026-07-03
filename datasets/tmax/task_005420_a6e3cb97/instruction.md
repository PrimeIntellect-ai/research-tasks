You are a network security engineer tasked with building a high-performance C-based traffic inspector to analyze decrypted HTTP traffic at the edge. 

Your workflow consists of two main stages: fixing a vendored dependency and building the traffic inspector.

**Stage 1: Fix and Compile the Vendored Parser**
We vendor our HTTP parser, `picohttpparser` (a fast C HTTP parser), in `/app/picohttpparser/`. However, the vendored version has a broken `Makefile` that prevents it from compiling.
1. Inspect and fix the `Makefile` in `/app/picohttpparser/`. 
2. Compile the parser into a shared library named `libpicohttpparser.so` inside `/app/picohttpparser/`.

**Stage 2: Build the Traffic Inspector**
Write a C program at `/home/user/traffic_inspector.c` and compile it to `/home/user/traffic_inspector`. 
It must link against your compiled `libpicohttpparser.so`.

The `traffic_inspector` must read a raw HTTP request from `stdin` until EOF, parse it using `picohttpparser`, and enforce the following security rules:

1. **Vulnerability Analysis (Injection/XSS):** Check the request URI. If it contains any of the following substrings (case-insensitive), it is considered malicious:
   - `<script`
   - `%3Cscript`
   - `UNION SELECT`
   - `%27%20OR`
2. **TLS/SSL Certificate Verification:** We rely on an upstream TLS terminator that injects the `X-SSL-Cert-Valid` header. If this header is missing, or its value is anything other than `SUCCESS`, the request must be treated as malicious.
3. **Sensitive Data Redaction:** For any request that passes the above checks, you must redact sensitive credentials before forwarding. Reconstruct and print the HTTP request to `stdout`. If an `Authorization` header is present, its value must be replaced entirely with the string `REDACTED`.

**Execution and Exit Codes:**
- If a request is flagged as malicious by rules 1 or 2, your program must print nothing to `stdout` and exit immediately with status code `1`.
- If a request is clean, it must print the (redacted) HTTP request to `stdout` and exit with status code `0`.

Ensure your C program handles standard HTTP methods, URIs, and headers correctly as parsed by `picohttpparser`. The automated verification suite will feed hundreds of raw HTTP files into your binary via standard input.
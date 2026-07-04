You are an integration developer building a pre-flight request validator for a new API gateway. The gateway routes requests using a legacy C-based routing engine, but we need to filter out malformed or malicious requests in Python before they reach the C backend.

There are three parts to your task:

**1. Fix the Legacy Router (Vendored Package)**
We have vendored the legacy C routing tool at `/app/vendored/uroute-0.5.1`.
It contains a `Makefile`, but compilation currently fails due to a linking error. 
- Fix the `Makefile` and compile the project to produce the `uroute_cli` executable.
- The compiled `uroute_cli` takes a URL path as its first argument (e.g., `./uroute_cli /api/v1/users`) and exits with code `0` if the route is valid, or a non-zero code if the route is unknown.

**2. Implement the Gateway Filter (Python)**
Write a Python script at `/home/user/gateway_filter.py` that takes a full URL string as its only command-line argument and prints exactly `ACCEPT` or `REJECT` to standard output. 

To `ACCEPT` a request, all of the following conditions must be met:
* **Checksum Validation:** The URL will contain a `chk` query parameter (a 2-character hex string). This checksum must equal the XOR-sum of the ASCII values of all characters in the URL's **path** (everything before the `?`). If it does not match, the request must be rejected.
* **Payload Emulation:** The URL will contain an `ops` query parameter, which is a hex-encoded string representing a custom bytecode sequence. You must implement a simple stack-based virtual machine to emulate this payload. 
  - `01 <byte>`: PUSH the next byte onto the stack.
  - `02`: ADD (pop two values, push their sum).
  - `03`: MUL (pop two values, push their product).
  - All values are unsigned 8-bit integers (wrap around on overflow). 
  - If the stack underflows, or if the final value at the top of the stack after execution is strictly greater than `100`, the payload is deemed malicious and must be rejected.
* **Route Validation:** If the request passes the checksum and emulator checks, your Python script must invoke the compiled `/app/vendored/uroute-0.5.1/uroute_cli` passing the URL's path. If the C tool returns a non-zero exit code, the request must be rejected.

**3. Test against the Corpora**
We have provided test requests in two directories:
- `/app/corpora/clean_requests/`: Contains text files (one URL per file) that your script MUST `ACCEPT`.
- `/app/corpora/evil_requests/`: Contains text files (one URL per file) that your script MUST `REJECT`.

You can use these files to test your script. Your final solution will be automatically evaluated against these corpora.
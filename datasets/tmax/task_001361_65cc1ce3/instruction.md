You are a web developer tasked with building a "sanitizing" reverse proxy and its associated test suite. 

We need to place a proxy in front of our legacy backend server. The legacy server crashes if it receives JSON payloads containing "private" keys (keys starting with an underscore `_`) and it requires all JSON object keys to be strictly alphabetically sorted for its caching layer to work.

Your task is to write a Python-based reverse proxy that intercepts incoming HTTP POST requests, deserializes the JSON payload, applies an algorithmic sanitization, serializes it back to JSON, and forwards the request to the upstream server.

Here are the exact requirements:

1. **The Sanitizer Function:**
   Write a module `/home/user/workspace/sanitizer.py` containing a function `sanitize_payload(json_bytes: bytes) -> bytes`.
   - It must deserialize the JSON bytes.
   - It must recursively traverse the parsed JSON structure (which could be a mix of dicts, lists, strings, numbers, etc.).
   - It must remove any dictionary keys that start with the underscore character (`_`), at any depth.
   - It must sort all dictionary keys alphabetically.
   - List order must remain completely unmodified.
   - It must serialize the result back to JSON bytes using a compact representation (no spaces between separators, i.e., `{"a":1,"b":2}`).

2. **Unit Tests:**
   Write a test suite in `/home/user/workspace/test_sanitizer.py` using `pytest`.
   - You must write at least three distinct test functions testing `sanitize_payload`.
   - The tests must cover: removing top-level underscore keys, removing deeply nested underscore keys, preserving list order, and sorting keys alphabetically.

3. **The Reverse Proxy:**
   Write a server script in `/home/user/workspace/proxy.py`.
   - It must listen for HTTP POST requests on `127.0.0.1:8080`.
   - When a POST request is received on any path, it must read the body, pass it through `sanitize_payload()`, and forward the POST request with the sanitized body to the upstream server at `http://127.0.0.1:9000` (preserving the original URL path).
   - Important: Set the `Content-Length` header of the forwarded request to match the length of the new sanitized body. Set the `Content-Type` to `application/json`.
   - Return the HTTP status code and exact response body from the upstream server back to the original client.

You may use standard Python libraries (like `http.server`, `urllib`, `json`) or popular third-party ones like `requests` and `Flask`/`FastAPI` if you install them. Do not use Nginx or HAProxy. The backend upstream server is already running for you on port 9000.

Leave the proxy running in the background when you are finished. Ensure `pytest /home/user/workspace/test_sanitizer.py` passes successfully. Create a file `/home/user/workspace/SUCCESS` containing the word "DONE" when you are finished.
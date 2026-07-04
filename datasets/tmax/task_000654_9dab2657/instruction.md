You are an engineer setting up a custom local CI validation step for a polyglot build system. A recurring issue in the CI pipeline is that Python test suites pass locally but fail in CI due to strict, undocumented import ordering constraints enforced by a legacy linter.

Your task is to implement a lightweight Python validation server and fix an existing file to pass the validation.

**Part 1: Fix the Target File**
There is a file at `/home/user/polybuild/src/app.py`. Edit this file so that all of its top-level module imports (`import X` or `from X import Y`) are strictly in ascending alphabetical order by module name.

**Part 2: The Validation Server**
Write a Python HTTP server at `/home/user/polybuild/server.py` that uses the standard `http.server` library (no external frameworks like Flask). The server must:
1. Listen on `127.0.0.1` port `8080`.
2. Handle `GET` requests to the `/validate` route.
3. Parse two URL query parameters: `target` (a base64-encoded string) and `crc` (an integer).
4. Decode `target` using Base64, and then decode the resulting bytes using the `iso-8859-1` (Latin-1) character encoding. This decoded string represents a file path (e.g., `/home/user/polybuild/src/app.py`).
5. Calculate the `zlib.crc32` checksum of the raw decoded Latin-1 bytes of the target. If the calculated checksum does not match the provided `crc` parameter, return an HTTP 400 Bad Request response.
6. If the checksum matches, start memory tracking using Python's built-in `tracemalloc` module.
7. Read the file at the decoded path and parse it using the `ast` module. Iterate through the AST to verify that the module names in all `Import` and `ImportFrom` nodes appear in strictly alphabetical order.
8. Stop memory tracking and retrieve the peak memory usage during the AST parsing step.
9. If the imports are out of order, return an HTTP 406 Not Acceptable response.
10. If the imports are correctly ordered, return an HTTP 200 OK response with a JSON payload in this exact format: `{"status": "pass", "peak_memory_bytes": <integer>}`.

Leave the server running in the background on port 8080 when you are finished. Ensure `/home/user/polybuild/src/app.py` is fixed before you complete the task.
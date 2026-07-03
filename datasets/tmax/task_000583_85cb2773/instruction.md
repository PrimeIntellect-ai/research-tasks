You are an open-source maintainer reviewing a pull request for a lightweight C-based REST API server. The PR implements a new rate-limiting module and request validation for the `/api/submit` endpoint. 

The contributor noted in the PR: "The test suite passes locally on my machine, but it segfaults and fails the rate-limit tests in the CI pipeline when compiled with optimizations (`-O3`)."

The source code is located in `/home/user/api_server`.

Here is what you need to do:
1. **Fix the Assembly Bug:** The rate limiter uses a custom hashing function in `hash.c` with inline x86_64 assembly for speed. The inline assembly is missing a crucial clobber register, causing Undefined Behavior (UB) when compiled with `-O3`. Analyze the assembly and add the missing clobber constraint so the hash is computed correctly.
2. **Fix the Memory Leak & Safety Issue:** In `api.c`, the request validation logic handles malformed payloads (e.g., missing the `Authorization` header). When a payload is invalid, the code rejects the request but fails to free the allocated `RequestContext` struct, causing a memory leak. Furthermore, there is a strict aliasing violation or uninitialized memory read when parsing the IP address. Fix these memory safety issues.
3. **Verify the Rate Limiter:** The rate limit should allow exactly 2 requests per IP, returning HTTP 200. The 3rd request must return HTTP 429 Too Many Requests.
4. **Testing:** You can build the server by running `make`. It produces `./server`.
5. **Reporting:** Once you have fixed the code, start the server in the background, send 3 valid requests to `http://127.0.0.1:8080/api/submit` with the header `Authorization: Bearer token123` from the same IP using `curl`. Write the HTTP status codes of the 3 requests, one per line, to `/home/user/api_server/test_results.log`.

Ensure your fixes compile cleanly with `make` (which uses `-Wall -Werror -O3`). Leave the fixed source files in the `/home/user/api_server` directory.
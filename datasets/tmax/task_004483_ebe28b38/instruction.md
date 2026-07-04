You are an open-source maintainer reviewing a pull request for `authproxy`, a Python-based reverse proxy designed to sit in front of web applications and sanitize incoming requests. The vendored package source is located at `/app/authproxy`.

The PR author added a `canonicalize_request` function in `/app/authproxy/normalize.py` to perform character decoding, Unicode normalization, and query string sorting to enforce a canonical request format (preventing HTTP smuggling and WAF bypasses). 

While the logic achieves the security goals and passes the functional tests, the PR introduces a massive performance regression. The author implemented the URL decoding and query parameter sorting from scratch using highly inefficient algorithms (e.g., $O(n^2)$ string manipulations and bubble sort). When processing large payloads, the proxy becomes a bottleneck.

Your task:
1. Examine the `canonicalize_request` function in `/app/authproxy/normalize.py`.
2. Refactor the implementation to be efficient (e.g., using Python's standard library functions for URL decoding and sorting) while maintaining the exact same functional behavior.
3. Ensure that the provided test suite (`pytest /app/authproxy/tests/test_normalize.py`) still passes perfectly. You may need to create or tweak test fixtures if you change internal interfaces, but the public behavior must remain identical.
4. Run the benchmark script `/app/authproxy/benchmark.py` to verify your performance improvements. The script prints the runtime in seconds.

To succeed, your refactored code must run fast enough to bring the benchmark execution time below `0.1` seconds, while keeping all tests green. Leave the optimized code in `/app/authproxy/normalize.py`.
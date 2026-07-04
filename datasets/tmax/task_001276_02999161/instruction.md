You are a web developer building a high-performance rate limiter feature to protect your API from DoS attacks. To achieve maximum performance, the core custom data structure (a Token Bucket) has been written in C, but it needs to be integrated into Python and rigorously tested to ensure there are no security flaws in the request calculation.

You have been given a workspace at `/home/user/rate_limiter/` containing:
- `bucket.c`: The C-extension source code for the Token Bucket logic.
- `limiter.py`: A Python wrapper class `TokenBucket` that interfaces with the C-extension.
- `setup.py`: A broken build script.

Your tasks are:
1. Fix the build system configuration in `/home/user/rate_limiter/setup.py` so that it correctly compiles `bucket.c` into a Python extension module named `_bucket`.
2. Build the extension in-place so that `import _bucket` works in the `/home/user/rate_limiter/` directory.
3. Write a property-based test in `/home/user/rate_limiter/test_limiter.py` using the `pytest` and `hypothesis` frameworks.
   - Your test must instantiate `TokenBucket(capacity=100, fill_rate=10)` (100 tokens max, 10 tokens added per second).
   - Use `hypothesis.given` to generate a list of integers representing elapsed time in seconds between consecutive requests (use `st.lists(st.integers(min_value=0, max_value=20), min_size=1, max_size=50)`).
   - Iterate through the list, calling `bucket.consume(1, elapsed_time)` for each.
   - Assert that the bucket's internal token count (accessible via `bucket.get_tokens()`) NEVER exceeds the capacity (100) and NEVER drops below 0.
4. Run your test using pytest and save the exact output to `/home/user/rate_limiter/test_report.log`.

Make sure to install any required Python packages (`pytest`, `hypothesis`) if they are missing.
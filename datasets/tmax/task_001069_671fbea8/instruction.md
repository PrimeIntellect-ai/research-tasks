I am migrating an old web service from Python 2 to Python 3. During the migration, we decided that the URL routing and parameter parsing module was a massive performance bottleneck. Instead of porting the slow Python 2 code directly to Python 3, we want to rewrite the core parsing logic as a C++ shared library, which we will then call via Python 3's `ctypes`.

Your task is to implement this C++ shared library, ensure its ABI is compatible with C-style callers, compile it, and write a Python 3 benchmark to test its performance.

Please perform the following steps:

1. **Write the C++ Shared Library**
Create a file at `/home/user/router.cpp` that implements URL routing and parameter parsing.
It must export a function with the exact C-linkage signature:
`void parse_route(const char* url, char* path, char* query)`

The function should process the `url` string:
- Everything before the first `?` character should be copied into the `path` buffer.
- Everything after the first `?` character should be copied into the `query` buffer.
- If there is no `?` character, the entire string goes to `path`, and `query` should be an empty string.
Assume `path` and `query` point to pre-allocated buffers of 256 bytes each. Do not worry about buffer overflows for this controlled environment.

2. **Compile the Library**
Compile `/home/user/router.cpp` into a shared library located at `/home/user/librouter.so`. It must be compiled to allow dynamic linking and avoid C++ name mangling so Python's `ctypes` can find `parse_route`.

3. **Benchmarking script**
Write a Python 3 script at `/home/user/benchmark.py` that:
- Loads `/home/user/librouter.so` using `ctypes`.
- Allocates the necessary string buffers (`ctypes.create_string_buffer(256)`).
- Calls `parse_route` 100,000 times in a loop using the test URL: `/api/v2/items?category=books&sort=desc`.
- Measures the total time taken for the loop using the `time` module.

4. **Execute and Log Results**
Run your benchmark script and save the output to `/home/user/benchmark_results.txt`.
The file must contain exactly three lines in this format:
```
Route: /api/v2/items
Query: category=books&sort=desc
Time: <time_in_seconds>
```
Where `<time_in_seconds>` is the numeric time taken for the 100,000 iterations (e.g., `0.045`).
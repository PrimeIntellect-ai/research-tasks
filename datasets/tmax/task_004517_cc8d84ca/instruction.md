You have been assigned to clean up, debug, and test a disorganized Python project located at `/home/user/project`. The project currently implements a custom URL routing and parameter parsing module, but it has severe architectural and memory issues. 

Currently, all files are dumped in the root directory:
- `/home/user/project/main.py`
- `/home/user/project/router.py`
- `/home/user/project/utils.py`

There are two primary problems you need to solve:

1. **Project Organization:**
   The files are unorganized. You must restructure the project into a standard Python package layout:
   - Create a `src/app` directory and move `main.py`, `router.py`, and `utils.py` into it.
   - Create empty `__init__.py` files in `src/` and `src/app/` to make them proper Python packages.
   - Create a `tests/` directory at the project root (i.e., `/home/user/project/tests/`).
   - Create an empty `__init__.py` in the `tests/` directory.

2. **Memory Leak and Testing:**
   Users have reported that the server process consumes memory indefinitely over time, especially when receiving requests with highly unique URL query parameters.
   - Profile or inspect `src/app/router.py`. You will find a custom `parse_url(url)` function that caches parsed parameters to speed up repeated queries.
   - Identify the global dictionary responsible for unbounded memory growth.
   - Fix the memory leak. Remove the global dictionary cache and instead use Python's built-in `functools.lru_cache` on the `parse_url` function, strictly setting `maxsize=128`.
   - Write a unit test suite in `/home/user/project/tests/test_router.py` using the standard `unittest` framework. You must write at least two tests:
     a) One testing basic parameter parsing (e.g., `parse_url("/api/data?user=admin&id=5")`).
     b) One verifying that the `lru_cache` is working (e.g., checking `parse_url.cache_info()`).

Finally, generate a report file at `/home/user/report.txt` with exactly two lines:
- Line 1: The absolute path to the reorganized router module.
- Line 2: The exact name of the global dictionary variable you removed to fix the memory leak.
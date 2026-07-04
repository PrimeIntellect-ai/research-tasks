I am the maintainer of a Python-based Web Application Firewall (WAF) proxy, and I'm currently reviewing a pull request from a new contributor. They attempted to optimize our payload inspection by rewriting our core signature-matching functions into a C extension. However, the PR is completely broken, and I need you to step in and fix it so we can merge.

The project is located at `/home/user/project`. 

Here is what you need to do to fix the PR:

1. **Fix the Makefile (`/home/user/project/ext/Makefile`)**:
   The contributor wrote a Makefile to build the C extension into a shared library (`libwaf.so`), but it fails to compile or link correctly. Fix the Makefile so that running `make` in that directory successfully produces `/home/user/project/ext/libwaf.so` using GCC. Note that it must be compiled as a shared library that can be loaded by Python's `ctypes`.

2. **Fix Memory Safety in C (`/home/user/project/ext/waf.c`)**:
   The C code includes a function `int check_xss(const char* payload, int len)`. It has a classic memory safety vulnerability (undefined behavior/out-of-bounds read) that causes segmentation faults on certain inputs. Identify and fix the out-of-bounds read.

3. **Code Translation**:
   We have a Python function `check_sqli(payload: str) -> bool` inside `/home/user/project/py_waf.py`. The contributor forgot to translate this into C. Translate this exact logic into `waf.c` as `int check_sqli_c(const char* payload)`. Ensure it returns `1` for a match and `0` otherwise. Recompile the extension after adding this.

4. **Test Fixture Setup (`/home/user/project/tests/test_waf.py`)**:
   The unit tests are broken because they try to make actual HTTP requests to an upstream server that doesn't exist. Modify `tests/test_waf.py` to use Python's `unittest.mock.patch` to mock `requests.get`. The mock should return a response object with a `status_code` of 200 and `text` of `"OK"`. Ensure `python3 -m unittest tests.test_waf` passes.

5. **Performance Benchmark**:
   Write a benchmarking script at `/home/user/project/benchmark.py` that compares the execution time of the Python `check_sqli` function versus the C `check_sqli_c` function (accessed via `ctypes` loaded from `ext/libwaf.so`). Run both functions 100,000 times on the string `"admin' OR 1=1 -- UNION SELECT * FROM users"`.
   Your script must write the results to `/home/user/project/bench_results.log` in exactly this format:
   ```
   PYTHON_TIME: <seconds>
   C_TIME: <seconds>
   C_IS_FASTER: <True/False>
   ```

Verify all steps are complete by ensuring the tests pass, the shared library exists, and the `bench_results.log` is generated correctly.
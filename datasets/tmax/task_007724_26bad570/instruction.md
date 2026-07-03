I am migrating our backend from Python 2 to Python 3. We have a custom C extension for parsing request headers and handling rate limiting that currently only works in Python 2 and has some known memory corruption issues when handling malformed inputs.

I need you to update and fix the C library located at `/home/user/py_ext/fast_req.c`. 

Here are your objectives:
1. **Memory Safety:** The current `parse_header` function allocates memory but has an off-by-one buffer overflow and a memory leak on error paths. Fix the undefined behavior and ensure there are no leaks.
2. **Conditional Build (Python 2 to Python 3 Migration):** Update the `extract_string` function. You must use conditional compilation macros (`#if PY_MAJOR_VERSION >= 3`). 
   - For Python 2 (`PY_MAJOR_VERSION == 2`), use the existing `PyString_AsString(obj)` mock logic.
   - For Python 3 (`PY_MAJOR_VERSION >= 3`), use the new `PyUnicode_AsUTF8(obj)` mock logic.
3. **Rate Limiting:** Implement the `check_rate_limit(uint32_t client_id, uint64_t current_time_ms)` function using a Token Bucket algorithm. 
   - The bucket capacity is 10 tokens.
   - The refill rate is 1 token per 100 milliseconds.
   - Return `1` if the request is allowed (and consume 1 token), or `0` if rate limited. State should be tracked per `client_id` (assume client_ids are integers from 0 to 99).
4. **Diff/Patch:** Once you have fixed `fast_req.c`, create a unified diff patch file named `/home/user/py_ext/migration.patch` comparing the original `fast_req.c.orig` to your updated `fast_req.c`.
5. **Testing:** Compile your code using the provided `/home/user/py_ext/Makefile` which builds a test executable `./test_ext`. Run it. If it passes, redirect its exact output to `/home/user/py_ext/success.log`.

The setup files are located in `/home/user/py_ext/`. 
Do not modify `python_mock.h`, `test_runner.c`, or `Makefile`. Only modify `fast_req.c`.
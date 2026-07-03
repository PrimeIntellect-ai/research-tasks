I need you to build a high-performance expression evaluation REST API. We are using a custom C-accelerated Python package called `fast-eval` which is vendored in `/app/fast-eval`. However, the package is currently broken and won't install. 

Please complete the following steps:

1. **Fix and Install the Vendored Package:**
   The `fast-eval` package located at `/app/fast-eval` uses a custom `setup.py` that invokes a `Makefile` in its `c_src/` directory to build a shared library (`libfasteval.so`). Currently, the build fails. Fix the `Makefile` (hint: it might be missing a flag required for shared libraries, or have a typo in the target). Once fixed, install the package globally or in the user environment so it can be imported via `import fast_eval`.

2. **Implement an Expression Parser:**
   The `fast_eval` package provides a single Python function: `fast_eval.compute(op: str, a: int, b: int) -> int` where `op` can be `"ADD"`, `"SUB"`, or `"MUL"`.
   You must write a Python parser that takes a string of chained operations, e.g., `"ADD(5, 3) | MUL(2) | SUB(4)"`. The parser should evaluate from left to right using a state machine:
   - Initial state: `ADD(5, 3)` = 8.
   - Next operation: `MUL(2)` applies to the previous result: `8 * 2 = 16`.
   - Next operation: `SUB(4)` applies to the previous result: `16 - 4 = 12`.
   The final output of this expression is `12`.

3. **Build the REST API:**
   Write a Python HTTP server using `Flask` or `FastAPI` (you can install them if needed) and save it to `/home/user/api.py`. It must:
   - Listen on exactly `127.0.0.1:8080`.
   - Expose a `POST /evaluate` endpoint.
   - Require an `Authorization: Bearer eval-secret-777` header. Return a 401 status code if missing or incorrect.
   - Accept a JSON body like: `{"expression": "ADD(10, 5) | MUL(3)"}`
   - Return a JSON response with the computed result: `{"result": 45}`.
   - Start the service in the background.

4. **Performance Benchmark:**
   Write a script at `/home/user/bench.py` that measures the time taken to evaluate `"ADD(1, 1) | MUL(2)"` 10,000 times by directly calling your parser and the `fast_eval.compute` function (not via HTTP). It should output a single line: `Benchmark completed: <time_in_seconds>s`. Run this script and append its output to `/home/user/bench_results.log`.
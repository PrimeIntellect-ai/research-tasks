You are acting as a release manager for a high-performance mathematical computing microservice. The service consists of a deeply optimized x86_64 assembly core, a C wrapper, and a Python REST API. The CI/CD pipeline is currently broken, and deployments are blocked. Your job is to fix the build, correct a mathematical error in the assembly code, implement the missing REST API logic, and verify the service by processing a batch of structured inputs.

Here is the state of the repository located at `/home/user/repo`:

1. **Build System Error:**
   The project uses CMake. The build configuration in `/home/user/repo/CMakeLists.txt` attempts to compile a C library (`libmathwrap.so`) that depends on a separately compiled assembly library (`libfastmath.so`). Currently, `libmathwrap.so` fails to build because it cannot find the shared assembly library at link time. Fix `CMakeLists.txt` so that `mathwrap` correctly links against `fastmath`. Compile the project in `/home/user/repo/build`.

2. **Assembly Mathematics Bug:**
   The assembly function in `/home/user/repo/src/fast_math.s` implements the mathematical polynomial $f(x, y) = 3x^2 + 2y$. It accepts two 64-bit integers (`x` in `%rdi`, `y` in `%rsi`) and returns the result in `%rax`. However, a bug in the assembly instructions causes it to incorrectly add a constant instead of multiplying. Analyze the minimal assembly file, identify the logical flaw, and patch it so it computes the polynomial exactly as $3x^2 + 2y$.

3. **REST API Construction:**
   The file `/home/user/repo/api/server.py` contains a skeleton Flask application. You must implement the POST `/compute` endpoint.
   - It should parse a JSON payload containing `x` and `y` (integer values).
   - Use Python's `ctypes` to load the newly built `/home/user/repo/build/libmathwrap.so`.
   - Call the C function `long compute_wrapper(long x, long y)` (which delegates to the assembly code).
   - Return the result as a JSON response: `{"result": <computed_value>}`.
   - Start the server on port `8080` (you can run it in the background).

4. **Structured Data Processing:**
   Once the service is running, read the structured inputs from `/home/user/repo/data/inputs.json`. This file contains an array of JSON objects: `[{"input_x": <val>, "input_y": <val>}, ...]`.
   Write a Python script to iterate over these inputs, map them to the `x` and `y` format expected by your REST API, send a POST request to `http://127.0.0.1:8080/compute` for each, and capture the results.
   
   Save the final combined output to `/home/user/output_results.json`. The output must be a strict JSON array of objects with exactly three keys: `x`, `y`, and `result`. 
   Format example:
   ```json
   [
     {"x": 2, "y": 3, "result": 18},
     {"x": 5, "y": 1, "result": 77}
   ]
   ```

To successfully complete the task, ensure `/home/user/output_results.json` is perfectly formatted and contains the correct mathematical computations, and that your fixed code remains in the repository.
You are an open-source maintainer reviewing a broken pull request for a mathematical microservice. The PR attempts to introduce a fast inverse square root endpoint using a C extension and a Flask API, but the continuous integration tests are failing. 

The repository is located at `/home/user/math_service`.

Here is the current state of the PR:
1. A C file `/home/user/math_service/fast_inverse_sqrt.c` implements the famous algorithm, but it needs to be compiled into a shared library named `libfastmath.so` in the same directory.
2. The Python wrapper `/home/user/math_service/math_ops.py` uses `ctypes` to call the C function, but the types are misconfigured, leading to segmentation faults or garbage numerical results.
3. The Flask application `/home/user/math_service/api.py` exposes an endpoint `/invsqrt/<value>` but fails to correctly parse the URL parameter as a floating-point number, causing internal server errors when passed to the math module.
4. The test file `/home/user/math_service/test_api.py` is missing a property-based test.

Your tasks are:
1. Compile `fast_inverse_sqrt.c` into a shared library `libfastmath.so` (ensure it is compiled with `-shared -fPIC`).
2. Fix the `ctypes` configuration in `math_ops.py` so the argument and return types match the C implementation exactly.
3. Fix the URL routing in `api.py` so the `/invsqrt/<value>` endpoint correctly receives a float and returns a JSON response: `{"result": <float>}`.
4. Implement a property-based test in `test_api.py` using the `hypothesis` library. The test function must be named `test_inv_sqrt_property`. It should generate random positive floats between `0.1` and `1000.0`, call the `get_inv_sqrt` function from `math_ops`, and assert that `1.0 / (result * result)` is within a 10% relative error margin of the original input.
5. Run the pytest suite and save the output to `/home/user/math_service/test_results.log`.

Make sure to install `Flask`, `pytest`, and `hypothesis` using `pip` before running the tests. Provide the final working state in the `/home/user/math_service` directory.
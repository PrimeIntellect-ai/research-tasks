You are an open-source maintainer reviewing a broken Pull Request. A contributor has added a new mathematical feature to your multi-language project located in `/home/user/math_api`.

The project structure is:
- `CMakeLists.txt`
- `src/math_ops.cpp`: Contains a C++ function `calculate_hypotenuse(double a, double b)`.
- `api/app.py`: A Flask REST API that loads the compiled C++ shared library via `ctypes` and exposes a route.
- `tests/test_api.py`: Pytest unit and integration tests.

Currently, the tests fail because:
1. The C++ library is built, but `ctypes` fails to find the `calculate_hypotenuse` symbol due to C++ name mangling (it lacks the proper C-ABI export).
2. The Flask URL routing in `api/app.py` has a bug: it fails to parse the URL parameters as numbers, causing `ctypes` to receive strings instead of `c_double` types.

Your task:
1. Fix `src/math_ops.cpp` so the function is exported with a C-compatible ABI.
2. Fix the Flask route in `api/app.py` so the parameters `a` and `b` in the route `/api/hypotenuse/<a>/<b>` are strictly parsed as floats.
3. Build the shared library. Create a `build` directory inside `/home/user/math_api`, run `cmake ..` and `make`.
4. Run the tests.
5. Save the standard output of `python3 -m pytest tests/test_api.py` to `/home/user/test_results.txt`.

Ensure all tests pass and the output file is generated correctly. Do not change the test file itself.
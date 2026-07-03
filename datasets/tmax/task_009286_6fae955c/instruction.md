You are a web developer working on a backend pricing feature. We have a Python module that fetches pricing rules from an internal API and evaluates them. For performance, the expression evaluation is written as a Python C-extension (`ceval`), but the package setup is currently broken and the test suite is missing.

Your task is to fix the build, write the missing tests with mocks, and verify the semantic versioning logic.

Here is your working directory: `/home/user/pricing_engine`

Inside, you will find:
1. `ceval.c`: The C-extension source code that evaluates simple prefix expressions (e.g., `ADD 5 10`).
2. `setup.py`: The build script for the package. It is currently broken and fails to compile the C-extension.
3. `engine.py`: The main Python module. It contains the `get_and_eval(api_ver)` function, which checks if the provided API version is at least "1.5.0" using semantic version comparison. If it is, it makes an HTTP GET request to `http://api.internal/rules?v={api_ver}`, extracts the "expression" field from the JSON response, and evaluates it using the `ceval` module.
4. `requirements.txt`: The required dependencies.

Please perform the following steps:
1. Fix `/home/user/pricing_engine/setup.py` so that it correctly defines and builds the `ceval` extension module from `ceval.c`.
2. Install the package and its dependencies in editable mode in the current environment.
3. Create a test file `/home/user/pricing_engine/test_engine.py` using `pytest`.
4. In `test_engine.py`, write two tests for the `get_and_eval` function:
   - **Test 1 (`test_version_too_low`)**: Call `get_and_eval("1.4.9")`. Assert that it returns `-1`. Use `unittest.mock.patch` to mock `requests.get` and assert that the mock was **not** called.
   - **Test 2 (`test_evaluate_success`)**: Call `get_and_eval("2.0.0")`. Use `unittest.mock.patch` to mock `requests.get` so that its `.json()` method returns `{"expression": "MUL 7 8"}`. Assert that `get_and_eval` returns `56`.
5. Create a shell script `/home/user/pricing_engine/run_tests.sh` that executes the tests via `pytest /home/user/pricing_engine/test_engine.py -v` and redirects the standard output to `/home/user/pricing_engine/test_results.log`. Make sure the script is executable.
6. Run `/home/user/pricing_engine/run_tests.sh`.

Ensure that the final `test_results.log` is generated and shows that both tests passed.
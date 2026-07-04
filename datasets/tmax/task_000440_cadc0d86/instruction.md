You are an open-source maintainer reviewing a broken Pull Request for a Python package called `fast-router`. This package parses custom routing rules, uses a Trie-like data structure, and includes an optional C-extension for performance. The PR contributor left the work unfinished, and the test suite is failing.

Your task is to fix the project located in `/home/user/fast-router` so that all tests pass, and the package can be conditionally built.

Here is what you need to fix:

1. **Structured Data Parsing (`router/parser.py`)**: 
   The `parse_routing_table(data: str)` function is supposed to parse a string of routing rules (one per line, format `PREFIX => DESTINATION`). Currently, it crashes if there are empty lines or comment lines (lines starting with `#`). Fix the function so it ignores empty lines and comments, returning a dictionary of `{prefix: destination}`.

2. **Test Fixture and Mock Setup (`tests/test_fetcher.py`)**:
   The `test_update_routes` function tests `fetch_and_parse()`, but it currently attempts to make a real HTTP request using `urllib.request.urlopen`. Modify the test using `unittest.mock.patch` to mock `urllib.request.urlopen` so that it doesn't hit the network. The mock should simulate a response whose `.read().decode('utf-8')` returns a JSON string: `'{"/api/v1": "backend-1", "/api/v2": "backend-2"}'`.

3. **Conditional Builds (`setup.py`)**:
   The package includes a C-extension (`router/_fast_router.c`) which is currently always compiled. Modify `setup.py` so that if the environment variable `PURE_PYTHON` is set to `"1"`, the C-extension is **omitted** from the `ext_modules` list, allowing a pure Python installation. If `PURE_PYTHON` is not `"1"`, it should build the extension normally.

4. **Testing and Verification**:
   Ensure `pytest` is installed (`pip install pytest`).
   You must run the tests under both build configurations and save their output.
   
   First, build and test the pure Python version:
   - Set `PURE_PYTHON=1`
   - Install the package: `pip install -e .`
   - Run the tests and redirect standard output to: `/home/user/test_pure_python.log`

   Second, build and test with the C-extension:
   - Set `PURE_PYTHON=0`
   - Install the package: `pip install -e .`
   - Run the tests and redirect standard output to: `/home/user/test_c_ext.log`

Both log files should show that all tests passed successfully.
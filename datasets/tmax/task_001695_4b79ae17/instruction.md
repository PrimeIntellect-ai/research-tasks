You are helping me fix and organize a Python project located at `/home/user/data_processor`. The project has several issues preventing it from building and passing its test suite in our CI environment. 

Here are the problems you need to solve:

1. **Checksum Verification**: The bash script `/home/user/data_processor/scripts/download_fixtures.sh` is supposed to download a test fixture (simulated by copying a local file) and verify its SHA256 checksum against a provided `.sha256` file. However, the checksum verification logic is broken. Fix the script so it correctly calculates the SHA256 hash of `fixture.dat` and compares it to the hash inside `fixture.dat.sha256`. The script should exit with status 0 if they match, and status 1 if they don't. Run the script to verify it works.

2. **Conditional Build Configuration**: The project has an optional C-extension for performance. The `setup.py` file is supposed to build this extension only when the environment variable `USE_C_EXT=1` is set. Currently, the `Extension` configuration in `setup.py` is pointing to the wrong source file path, causing the build to fail. Fix `setup.py` so that the `Extension` correctly points to `data_processor/fast_hash.c`. Then, build the extension in-place by running: `USE_C_EXT=1 python setup.py build_ext --inplace`.

3. **Import Ordering and Test Fixtures**: The test suite passes locally when tests are run individually, but fails in CI due to an import ordering issue. In `data_processor/utils.py`, a configuration value is evaluated at import time from `data_processor.config`. If a test imports `utils` before the CI configuration is initialized, it caches the wrong environment mode. 
   Refactor `data_processor/utils.py` to evaluate the mode dynamically (e.g., using a `get_mode()` function) instead of a module-level constant. Update `/home/user/data_processor/tests/test_processing.py` to use a pytest fixture to mock or initialize the CI environment correctly before calling `get_mode()`, and assert that it returns `"ci"`.

4. **Run and Log**: Once everything is fixed, run the test suite using `pytest /home/user/data_processor/tests/` and save the output to `/home/user/test_results.txt`.

Ensure all code changes are saved and the C-extension `fast_hash` is successfully built as a `.so` file in the `data_processor` directory.
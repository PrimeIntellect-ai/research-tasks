I need you to fix and test a high-performance Python package used for XSS sanitization, called `fast_sanitizer`. It is backed by a custom C library, but the package is currently broken and failing to build due to linking issues. After fixing it, you'll need to translate a test payload generator and run our integration test suite, converting the final output to a specific format.

All files are located in `/home/user/workspace`. 

Here are the specific phases of the task:

**Phase 1: Patch and Build the Underlying C Library**
1. Navigate to `/home/user/workspace/c_src`. There is a custom C library here called `htmlparser`.
2. A security vulnerability was found in this parser. Apply the patch file `/home/user/workspace/c_src/security_fix.patch` to `htmlparser.c`.
3. Run `make` to compile the shared library (`libhtmlparser.so`). 

**Phase 2: Fix the Python Package build**
1. Navigate to `/home/user/workspace/python_pkg`. This directory contains a broken `setup.py` for the `fast_sanitizer` Python package.
2. The `setup.py` currently fails to compile because it cannot find the `htmlparser.h` header, nor can it link against the `htmlparser` library you just built. 
3. Fix `setup.py` by modifying `include_dirs`, `library_dirs`, and `runtime_library_dirs` to point to the absolute path of the built C library (`/home/user/workspace/c_src`).
4. Install the package into your current Python environment (e.g., using `pip install -e .`). 

**Phase 3: Code Translation**
1. We have a test payload generator written in Node.js located at `/home/user/workspace/tests/payloads.js`.
2. Translate the logic of `payloads.js` into a Python module named `/home/user/workspace/tests/payloads.py`. 
3. The new Python module must contain a function `get_payloads()` that returns exactly the same list of dictionaries as the JavaScript module.

**Phase 4: Integration Testing and Data Transformation**
1. Once `fast_sanitizer` is installed and `payloads.py` is ready, run the test script `/home/user/workspace/tests/test_runner.py`.
2. This script will generate an XML report of the sanitization results at `/home/user/workspace/tests/results.xml`.
3. Parse this XML file and transform it into a JSON file at `/home/user/workspace/summary.json`.
4. The JSON file must be an array of objects, each containing:
   - `"id"`: The integer ID of the payload (from the XML).
   - `"original"`: The original string payload.
   - `"sanitized"`: The sanitized string payload.
   - `"is_safe"`: A boolean. Set this to `true` if the sanitized string does NOT contain the substring `<script>`, and `false` if it still contains `<script>`.

Ensure the final JSON is valid and strictly follows the structure described above.
You are a mobile build engineer maintaining a CI pipeline. We have a C-based string utility (`string_processor.c`) used by our Python build scripts via `ctypes`. Due to cross-compilation circular dependencies during the pipeline setup, we want to replace this C function with a pure Python implementation. However, the new Python code must be a 100% accurate translation of the C logic.

Your task is to:
1. Translate the C function found in `/home/user/project/string_processor.c` into a pure Python function named `process_string_py(input_str: str) -> str`. Append this new function to `/home/user/project/pipeline_util.py`.
2. Write a property-based test using the `hypothesis` and `pytest` libraries in a new file `/home/user/project/test_processor.py`. The test must:
   - Generate random strings (you can restrict the alphabet to standard ASCII characters for simplicity, e.g., `characters(min_codepoint=32, max_codepoint=126)`).
   - Pass the strings to both `process_string_c` (already in `pipeline_util.py`) and your new `process_string_py`.
   - Assert that the outputs are identical.
3. Generate a unified diff patch file at `/home/user/project/pipeline.patch` that represents the changes you made to `pipeline_util.py` (comparing the original file to your modified version).
4. Create a CI script at `/home/user/project/run_ci.sh` that:
   - Compiles `string_processor.c` into a shared library `libstring_processor.so` using `gcc`.
   - Runs `pytest /home/user/project/test_processor.py`.
   - If the tests pass, prints "CI PASS" to standard output.

Environment:
- The project directory is `/home/user/project/`.
- Assume `pytest` and `hypothesis` can be installed via `pip install pytest hypothesis`.

Verify your work by running your `run_ci.sh` script and ensuring the property-based tests pass and output "CI PASS".
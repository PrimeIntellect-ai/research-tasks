You are a platform engineer maintaining a CI/CD pipeline. The current pipeline for a native C-library project is broken due to incorrect build orders, missing test fixtures, and failing tests. 

Your objective is to fix the build process, execute the foreign-function interface (FFI) tests, and verify the output.

Perform the following steps in `/home/user/project`:

1. **Dependency Resolution**:
   You have a file `deps.txt`. Each line defines a build relationship in the format `Dependency Target` (meaning `Dependency` must be built before `Target`). Use a topological sort to determine the correct build order.

2. **Compilation**:
   Write a bash script `/home/user/project/build.sh` that reads this sorted order and compiles the corresponding C files from `src/` into shared libraries (`.so` files) inside the `bin/` directory. 
   - Use `gcc -shared -fPIC`.
   - Ensure you link dependent libraries correctly (e.g., if compiling `libA.so` which depends on `libB`, include `-L./bin -lB`).

3. **Test Fixture Setup**:
   The test suite relies on a mock configuration. Create a file `/home/user/project/mock_config.json` with the exact following content:
   `{"environment": "CI", "strict_mode": true}`

4. **Testing and Diffing**:
   A Python script `/home/user/project/test_runner.py` uses `ctypes` to load the compiled `libA.so` from the `bin/` directory and execute it. 
   - Run the test runner (ensure it can find the compiled shared libraries).
   - Capture the standard output of the test runner.
   - Sort the output lines alphabetically.
   - Sort the lines of `/home/user/project/expected.txt` alphabetically.
   - Run a unified diff (`diff -u`) between the sorted expected output and the sorted actual output.
   - Save the exact output of the diff command to `/home/user/project/test_diff.patch`.

Make sure all created scripts are executable. If you are successful, the `test_diff.patch` file will be empty, indicating the outputs matched perfectly.
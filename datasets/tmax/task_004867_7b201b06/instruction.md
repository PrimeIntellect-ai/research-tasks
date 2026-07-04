You are a platform engineer maintaining CI/CD pipelines. A custom Python C-extension used extensively in your pipeline's data aggregation step has been causing intermittent segmentation faults and incorrect results, causing pipeline failures.

The project is located at `/home/user/project`.

Your tasks:
1. **Fix the C Memory Safety Bug**: Inspect `/home/user/project/libcalc.c`. The function `sum_array` has a memory safety bug (undefined behavior/out-of-bounds read) that causes incorrect sums or crashes. Identify and fix the bug.
2. **Fix the Build System**: The extension isn't linking properly because the build configuration in `/home/user/project/setup.py` is incomplete. It fails to include all necessary source files to compile the `calc_ext` module. Update `setup.py` so it properly builds the extension.
3. **Write Property-Based Tests**: Open `/home/user/project/test_calc.py`. Write a property-based test using the Python `hypothesis` library. 
   - Import the `calc_ext` module.
   - Use `@given` and `hypothesis.strategies` to generate lists of integers (you can constrain the integers to `min_value=-1000, max_value=1000` to avoid standard C integer overflow).
   - Test that `calc_ext.sum_array(generated_list)` equals Python's built-in `sum(generated_list)`.
4. **Build and Test**: 
   - Compile the extension in-place (`python setup.py build_ext --inplace`).
   - Run the tests using `pytest test_calc.py > /home/user/project/test_log.txt`.

Ensure that the test passes and the final output is captured in `/home/user/project/test_log.txt`.
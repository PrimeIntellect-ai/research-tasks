I am organizing an old project in my workspace, but the build process is broken and the test suite is failing. The project is located in `/home/user/math_optimizer/`. 

It consists of a C shared library (`libmathops.so`) that performs fast matrix transformations, and a Python wrapper that uses `ctypes` and `hypothesis` for property-based testing. 

I need you to fix the project by completing the following tasks:

1. **Vision and Versioning**: There is an image located at `/app/requirements.png` that contains handwritten notes about the required minimum semantic version for the C library. Read this version constraint from the image.
2. **Build System Repair**: The `Makefile` in `/home/user/math_optimizer/` is broken. It fails to build `libmathops.so` because it cannot find the standard math library at link time, lacks position-independent code flags, and doesn't create a shared object correctly. Fix the `Makefile` so that running `make` successfully builds `libmathops.so`. You must also enable standard C compiler optimizations (`-O3`) because the tests are currently timing out.
3. **Property-Based Testing Integration**: In `/home/user/math_optimizer/test_ops.py`, complete the Python script. It needs to:
    - Load `libmathops.so`.
    - Extract the library's compiled version string (using the `get_version()` C function).
    - Compare the C library's version against the semantic version parsed from `/app/requirements.png`. The test should assert that the library version is greater than or equal to the requirement.
    - Run the existing `hypothesis` property-based tests that verify the matrix transformations.
4. **Performance Metric**: Run your test suite. Once it passes, write a Python script `/home/user/math_optimizer/benchmark.py` that measures the execution time of running the `matrix_transform` C function 1,000,000 times with a random 3x3 matrix. Save the average execution time (in seconds) as a floating-point number in `/home/user/math_optimizer/metric.txt`.

Ensure all dependencies are met. Your final output should be a working `Makefile`, a passing `test_ops.py`, and the `metric.txt` file containing the benchmark time.
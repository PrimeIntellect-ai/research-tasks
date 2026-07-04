You are a mobile build engineer maintaining a cross-platform C++ pipeline. We have a numerical optimization library used for edge devices that implements a custom `FixedVector` data structure and a constraint satisfaction algorithm.

Currently, the CI pipeline is broken in three ways:
1. **Linkage Error**: The `CMakeLists.txt` in `/home/user/project` is configured incorrectly. The test executable `test_app` fails to link against the shared library `math_lib` because the linking instruction is missing.
2. **Algorithmic Bug**: The `solve_constraint` function in `/home/user/project/src/math_lib.cpp` attempts to adjust the elements of a `FixedVector` so their sum equals a `target_sum`, while keeping all elements non-negative. However, it crashes or produces incorrect results due to an out-of-bounds access bug (a classic off-by-one error).
3. **Missing Testing**: We need a property-based test to ensure this bug doesn't return. 

Your tasks:
1. Fix `/home/user/project/CMakeLists.txt` so that `test_app` links correctly against the `math_lib` shared library.
2. Fix the out-of-bounds bug in `/home/user/project/src/math_lib.cpp`. The loop should iterate exactly over the valid elements of the vector (which has a fixed capacity defined by `v.size()`).
3. Modify `/home/user/project/test/test_app.cpp` to include a custom property-based test. The test must:
   - Generate 100 random `FixedVector` instances (size 5). You can populate them with random positive integers modulo 20.
   - Call `solve_constraint(v, 100)` on each.
   - Verify that the sum of the elements in each vector is exactly 100, and no element is negative.
   - If all 100 vectors satisfy this property, write the exact string `PROPERTY_TEST_PASSED` to a new file at `/home/user/project/test_result.log`. If any fail, write `PROPERTY_TEST_FAILED`.

To verify your solution, you should compile the project using CMake in the `/home/user/project/build` directory, run the `test_app`, and ensure that `/home/user/project/test_result.log` contains the success message.
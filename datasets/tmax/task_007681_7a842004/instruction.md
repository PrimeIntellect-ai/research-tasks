I am building a Rust application that needs to perform some heavy mathematical computations. To do this, I am attempting to bind a legacy C library (`math_lib_c`) using Rust's Foreign Function Interface (FFI). However, I am running into several build and runtime issues, and I need you to fix them and complete the integration.

The workspace is located at `/home/user/workspace/`. It contains:
1. `math_lib_c/`: A C library directory with `matrix_math.c`, `matrix_math.h`, and a `Makefile`.
2. `rust_app/`: A Rust binary project that should link to this C library.
3. `verifier.py`: A Python script containing the reference mathematical implementation for matrix multiplication and trace calculation.

Your objectives are:

**Phase 1: Fix the C Library Build and Memory Safety**
The C library calculates the product of two square matrices. 
1. The `Makefile` in `/home/user/workspace/math_lib_c` is broken. It is supposed to compile the C code into a shared object named `libmatrixmath.so`. Modify the `Makefile` so that running `make` successfully produces `libmatrixmath.so` in the `math_lib_c` directory. Make sure it compiles with position-independent code (PIC).
2. The `multiply_matrices` function in `matrix_math.c` causes a segmentation fault due to a severe memory allocation bug (Undefined Behavior). Identify and fix the memory safety issue in the C code. 

**Phase 2: Build System and Semantic Versioning**
1. In `rust_app`, create or update `build.rs` to configure Cargo to dynamically link against `libmatrixmath.so` located in the `math_lib_c` directory.
2. The C library exposes a function `const char* get_version()`. In your Rust application's initialization, call this function via FFI. Implement a semantic version check in Rust: the application must successfully proceed ONLY if the C library's version is `>= 1.2.0` and `< 2.0.0`. If it does not match, the Rust program should panic.

**Phase 3: Code Translation and Execution**
1. Translate the verification logic found in `/home/user/workspace/verifier.py` into Rust.
2. In `rust_app/src/main.rs`, define two 5x5 matrices (flattened as 1D arrays of 25 elements).
   Matrix A should be: `[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25]`
   Matrix B should be: `[25, 24, 23, 22, 21, 20, 19, 18, 17, 16, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1]`
3. Pass these arrays to the C library's `multiply_matrices` function via FFI. 
4. Calculate the trace (sum of the main diagonal) of the resulting matrix using the Rust translation of the verifier logic.
5. Write the final calculated trace as a plain integer string to `/home/user/workspace/result.txt`.

Ensure your Rust code handles the unsafe FFI boundaries correctly and frees any C-allocated memory if necessary (the C header exports `free_matrix`).
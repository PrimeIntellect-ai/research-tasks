You are a developer stepping in to fix a failing Rust project located at `/home/user/app`. 
The project relies on a custom native C library called `mathops`, but the build is failing due to an environment misconfiguration and linker/compiler errors.

Your goals are to:
1. **Fix the Environment and Build**: The `mathops` library (compiled as a static library) and its `pkg-config` file are located somewhere in `/home/user/custom_lib/`. The project's `build.rs` uses the `pkg-config` crate to find it. You must fix the environment misconfiguration so that `cargo build` successfully locates and links the library. Do not modify `build.rs` or move the C library files; instead, configure your environment variables correctly.
2. **Fix Compiler Errors**: Once the build script passes, you will encounter a Rust compiler error in `src/lib.rs` related to borrowing rules in the `process_data` function. Interpret the error and fix the code so it compiles without changing the function signature.
3. **Construct a Regression Test**: Create a test module in `src/lib.rs` and write a test named `test_process_data_regression`. The test should:
   - Create a `Vec<i32>` containing `[10, 20]`.
   - Call `process_data` on it.
   - Use an `assert_eq!` macro to validate that the vector now contains `[10, 20, 10]`.
4. **Capture the Results**: Run `cargo test` and redirect the full output (both stdout and stderr) to a file named `/home/user/test_output.txt`.

Ensure your test passes and the file `/home/user/test_output.txt` is created with the successful test run output.
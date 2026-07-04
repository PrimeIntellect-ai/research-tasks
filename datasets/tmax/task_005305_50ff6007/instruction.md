I'm working on a data processing pipeline in `/home/user/data_pipeline`. It's a polyglot project: a Rust application that delegates heavy numerical processing to a C++ backend library via FFI. 

Currently, the project is completely broken. When I try to run `cargo test`, I encounter two major issues:
1. The project fails to compile because the build orchestration in `build.rs` incorrectly attempts to compile the C++ source file as plain C, leading to linker errors (missing C++ standard library).
2. Once the build system is fixed, the C++ code itself has a missing standard header causing a compilation error, and a memory safety bug (off-by-one array access resulting in undefined behavior) that causes `cargo test` to fail with a segmentation fault.

Your task:
1. Fix the build system (`build.rs`) to properly compile the C++ code.
2. Fix the missing header and the undefined behavior/memory safety issue in `cpp_src/processor.cpp`.
3. Verify the fix by running the test suite (`cargo test`).
4. Once tests pass, run the program to process some data by executing: `cargo run -- 10.5 20.2 30.3 > /home/user/result.log`

Ensure your fixes leave the code robust and correctly functioning. The final output must be written to `/home/user/result.log`.
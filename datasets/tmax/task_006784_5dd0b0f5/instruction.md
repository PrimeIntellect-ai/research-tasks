You have been given access to a hybrid Rust/C++ repository located at `/home/user/data_app`. The application is a REST API written in Rust that delegates heavy data processing to a C++ engine via FFI. 

Currently, the project is completely broken. The original developer left it in an uncompilable state with memory safety issues. Your task is to fix the application, ensure it runs reliably, and benchmark its data processing endpoint.

Here is the directory structure:
```
/home/user/data_app
├── cpp_engine
│   ├── CMakeLists.txt
│   ├── processor.cpp
│   └── processor.h
├── rust_server
│   ├── Cargo.toml
│   ├── build.rs
│   └── src
│       └── main.rs
└── benchmark.sh
```

Your objectives are:
1. **Fix the Build System**: The Rust project (`rust_server`) fails to compile because its `build.rs` relies on the C++ CMake project, which is misconfigured. You must fix `/home/user/data_app/cpp_engine/CMakeLists.txt` so that it produces a static library (`libprocessor.a`) with Position Independent Code (-fPIC) enabled, rather than an executable.
2. **Fix C++ Memory Safety & UB**: Once compiling, the Rust test suite (`cd /home/user/data_app/rust_server && cargo test`) will crash due to a segmentation fault and memory leaks in the C++ data processing logic. Identify and fix the undefined behavior and memory leaks in `/home/user/data_app/cpp_engine/processor.cpp`. Do not change the function signature in `processor.h`.
3. **Run the Server and Benchmark**: 
   - Start the Rust REST API server locally on port `3000` (it runs in the background or you can use a separate terminal session).
   - Execute the `/home/user/data_app/benchmark.sh` script, which will send 1000 requests to the `/process` endpoint.
   - The script will automatically generate a file at `/home/user/benchmark_results.json`. Ensure this file is created successfully.

You have succeeded when `cargo test` inside `/home/user/data_app/rust_server` passes 100% of its tests, and `/home/user/benchmark_results.json` exists and contains successful HTTP 200 responses.
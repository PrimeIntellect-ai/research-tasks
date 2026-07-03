You are an open-source maintainer reviewing a recent Pull Request for your C++ project, `LogParser`. A contributor added a new state machine-based log parser, but the CI build and tests are currently failing. 

The project is located at `/home/user/project`. 

There are two primary issues you need to resolve:
1. **Build Failure**: The project uses CMake, but it currently fails to link against a pre-compiled shared library `libsyslogger.so` located at `/home/user/deps/lib`. The header is in `/home/user/deps/include`. You need to fix `/home/user/project/CMakeLists.txt` so that it successfully finds and links this library.
2. **Runtime Crash**: Once compiled, running the `./parser` executable causes a segmentation fault. The contributor recently transitioned the code to use C++14 `std::unique_ptr` for memory safety, but introduced an ownership/borrowing bug (similar to a use-after-free) in the state machine loop inside `/home/user/project/main.cpp`. 

Your task:
1. Fix the `CMakeLists.txt` so the project successfully compiles. (Note: Ensure the binary can find the shared library at runtime, for example by using `LD_LIBRARY_PATH` when running it, or by modifying the CMake RPATH settings).
2. Find and fix the unique pointer ownership bug in `main.cpp` that causes the segfault. Do not change the underlying logic of what is being parsed or printed, just fix the crash.
3. Build the project in `/home/user/project/build`.
4. Run the compiled `parser` binary from the build directory. It will automatically read `/home/user/project/input.log`.
5. Redirect the standard output of the parser to a file named `/home/user/parsed_logs.txt`.

The automated tests will verify that `/home/user/parsed_logs.txt` exists and contains the correct, alphabetically sorted, successfully parsed log messages.
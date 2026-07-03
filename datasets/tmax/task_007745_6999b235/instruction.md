You are a platform engineer maintaining a CI/CD pipeline. One of the pipeline steps builds a C++ utility that parses a simple serialized payload using a custom state machine.

Currently, the build is failing in the `/home/user/ci_project` directory. 
There are two major issues you need to resolve:
1. **Compilation Failure**: The project fails to compile because it uses modern C++ features but the `Makefile` is missing the appropriate standard flag.
2. **Lifetime/Memory Issue**: Even if you fix the compilation, the program has a memory lifetime bug (specifically, dangling `std::string_view` references pointing to a destroyed temporary object) that causes undefined behavior and garbled output.

Your task:
1. Fix the `Makefile` in `/home/user/ci_project` so that the project compiles cleanly using `make`.
2. Debug and fix the C++ code in `/home/user/ci_project` to resolve the lifetime issue safely.
3. Compile the project using `make`.
4. Run the resulting `./app` binary.

If successful, the application will correctly parse the payload and write its output to `/home/user/ci_project/output.log`. You must ensure that the `app` runs successfully and generates this log file with the uncorrupted parsed values.
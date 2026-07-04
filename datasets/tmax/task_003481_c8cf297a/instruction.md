You are tasked with debugging a failing build for a C++ project. 

Our CI pipeline recently failed during a containerized build. The logs from the containerized CI run have been dumped locally to `/home/user/ci_logs/container_build.log`.

The project is located in `/home/user/project/`. It relies on a custom C++ build tool (`src/codegen.cpp`) to parse a configuration file (`data/config.txt`) and generate a C++ header (`build/config.h`) before compiling the main application (`src/main.cpp`). 

However, a recent addition to the `data/config.txt` file introduced an edge-case that the format parser doesn't handle correctly, causing the subsequent C++ compilation of `main.cpp` to fail.

Your tasks are:
1. Inspect the container build log to diagnose the build failure.
2. Fix the format parsing logic in `/home/user/project/src/codegen.cpp`. The parser must be updated to correctly ignore empty lines and comment lines (any line where the first non-whitespace character is `#`).
3. After fixing the code generator, verify the fix by running `/home/user/project/build.sh`.
4. Run the successfully compiled application (`/home/user/project/build/app`) and redirect its standard output to `/home/user/project/build/success.out`.

To complete the task successfully, `/home/user/project/build/success.out` must contain the output of the fixed and compiled application.
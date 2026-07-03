As a web developer, I am building a backend feature that requires high-performance prime factorization. To achieve this, I've written a concurrent prime factorization engine in Go, which I intend to call from a Python API wrapper using `ctypes`. 

However, my polyglot build orchestration is currently broken. I have a build script located at `/home/user/math_feature/build.sh` that is supposed to compile the Go code and run the Python wrapper to test it, but it's failing because the Go library isn't being compiled into a proper C-shared library format that Python can load.

Here is the directory structure inside `/home/user/math_feature/`:
- `prime_worker.go`: Contains the Go code with concurrency patterns to quickly factorize numbers, exporting a C-compatible function.
- `main.py`: A Python script that loads the compiled Go library and uses it to factorize the number `1234567890`. It writes the result to a file.
- `build.sh`: The broken shell script responsible for orchestrating the build and execution.

Your task is to:
1. Fix the build step in `/home/user/math_feature/build.sh` so that it correctly compiles `prime_worker.go` into a C-shared library named `libprimes.so` in the same directory.
2. Run `/home/user/math_feature/build.sh`.
3. Verify that the Python script successfully executes and writes the correct comma-separated prime factors to `/home/user/math_feature/output.txt`.

Do not modify `prime_worker.go` or `main.py`. Focus entirely on fixing the bash build script to ensure the correct compilation mode is used for polyglot interoperability.
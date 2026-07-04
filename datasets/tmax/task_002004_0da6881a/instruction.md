I am an open-source maintainer reviewing a PR that attempts to optimize our data processing pipeline by moving the core string-hashing logic into a C extension. However, the contributor's PR is broken and the build is failing. I need you to step in, fix the code, wrap it in Python, and set up a CI/CD configuration so we can test it properly.

Here is what you need to do:

1. **Fix the Vendored Package:**
   The contributor's C package is located at `/app/c-string-hasher`. When you try to run `make` inside that directory, it fails to build `libhasher.so` because of a circular import (header inclusion) between `hash.h` and `util.h`. 
   - Analyze the C headers and fix the circular inclusion by using proper forward declarations or adjusting the `#include` directives so that `make` succeeds and produces `/app/c-string-hasher/libhasher.so`.

2. **Write the Python FFI Wrapper:**
   Create a Python script at `/home/user/process.py`. This script must:
   - Use the `ctypes` module to load `/app/c-string-hasher/libhasher.so`.
   - Accept exactly one string argument from the command line (e.g., `python3 /home/user/process.py "mydata"`).
   - Pass this string to the C library's `compute_hash` function (which takes a `const char*` and returns a `char*`).
   - Print the returned string exactly as-is to standard output.
   - Ensure you properly handle memory if the C function allocates the returned string (the C library exposes a `free_hash_result(char*)` function for cleanup).

3. **Set up the CI/CD Pipeline:**
   We need a GitHub Actions workflow to ensure this doesn't break again. Create a YAML file at `/home/user/repo/.github/workflows/ci.yml`.
   The workflow must:
   - Be named `C-Extension CI`
   - Trigger on `push` and `pull_request` to the `main` branch.
   - Have a single job named `build-and-test` running on `ubuntu-latest`.
   - Contain steps to:
     1. Checkout the repository (use `actions/checkout@v3`).
     2. Run `make` in the `c-string-hasher` directory.
     3. Run a test step executing `python3 process.py "test_string"`.

Do not modify the core logic of the C functions, only the header file structure to fix the build errors.
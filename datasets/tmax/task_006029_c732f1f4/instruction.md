You are an engineer tasked with fixing a broken polyglot build process for a Python-based mathematical library called `polymath`. This library computes Fibonacci numbers using fast matrix exponentiation modulo `M`, implemented in C for performance.

The project is located at `/home/user/polymath`.

Currently, the build is failing because:
1. The C extension requires a header file (`src/constants.h`) that must be dynamically generated from a JSON configuration file.
2. The `setup.py` file is incomplete and fails to build the C extension (`fib_ext`).
3. The CI/CD script is incomplete.

Your tasks are:
1. **Create a data transformation script:** Write a Python script at `/home/user/polymath/generate_headers.py`. It must read `/home/user/polymath/data/matrix.json` and generate `/home/user/polymath/src/constants.h`. 
   For each key-value pair in the JSON (e.g., `"M00": 1`), the C header should contain a macro definition (`#define M00 1`).
2. **Fix `setup.py`:** Edit `/home/user/polymath/setup.py` so that it properly uses `setuptools.Extension` to compile `/home/user/polymath/src/fib.c` into an extension module named `fib_ext`.
3. **Setup a local CI pipeline:** Complete the bash script `/home/user/polymath/ci_build.sh`. When executed, this script must:
   - Run your `generate_headers.py` script.
   - Build the python wheel using `python3 setup.py bdist_wheel`.
   - Install the built wheel locally using `pip install dist/*.whl --force-reinstall`.
   - Execute a test using `python3 -c "import fib_ext; print(fib_ext.fib(10))"` and redirect the exact standard output of this command to `/home/user/polymath/ci_result.txt`.

Ensure all files are correctly placed and `ci_build.sh` is executable. Finally, run `./ci_build.sh` to produce the `ci_result.txt` file.
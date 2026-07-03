You are a build engineer responsible for creating a custom, polyglot build orchestration tool and managing the resulting artifacts. 

You have been given a workspace at `/home/user/project` containing a mixed-language project (C and Python). 
Your goal is to write a Python orchestrator that resolves the build dependencies, compiles the C code into shared libraries, runs a unit test suite, and packages the artifacts for release, finally hosting them via a local system service.

The workspace contains:
1. `/home/user/project/src/math_ops.c`: Contains basic math operations.
2. `/home/user/project/src/transform.c`: Contains data transformation logic.
3. `/home/user/project/deps.json`: A JSON file representing the dependency graph of the modules.

Perform the following steps:

**Phase 1: Algorithmic Build Orchestration**
Write a build script `/home/user/project/build_orchestrator.py`. This script must:
1. Parse `/home/user/project/deps.json`.
2. Perform a Topological Sort to determine the correct build order of the modules. 
3. Write the computed build order (a comma-separated list of module names, e.g., `mod1,mod2,mod3`) to `/home/user/project/build_order.txt`.
4. Compile the C source files into shared libraries (`.so` files) in the exact order determined by the topological sort. 
   - Compile `math_ops.c` into `libmath_ops.so`.
   - Compile `transform.c` into `libtransform.so`.
   - Use `gcc -shared -fPIC` for compilation. Store the `.so` files in `/home/user/project/build/`.

**Phase 2: Polyglot Integration & Testing**
Write a Python wrapper and test file `/home/user/project/test_integration.py` that:
1. Uses `ctypes` to load both `libmath_ops.so` and `libtransform.so` from the `build` directory.
2. Defines a `pytest` test suite that verifies:
   - `math_ops.c` has a function `int add(int, int)`. Test that `add(5, 7) == 12`.
   - `transform.c` has a function `int double_val(int)`. Test that `double_val(10) == 20`.
3. Your `build_orchestrator.py` must automatically invoke `pytest /home/user/project/test_integration.py`. If the tests fail, the build script should exit with a non-zero status code.

**Phase 3: Artifact Management & Services**
If the tests pass, the `build_orchestrator.py` must:
1. Create a distribution archive at `/home/user/project/artifacts/release.tar.gz` containing `libmath_ops.so`, `libtransform.so`, and `test_integration.py`.
2. Generate a JSON manifest at `/home/user/project/artifacts/manifest.json` with the SHA256 hashes of the three files included in the tarball. The format must be exactly:
   ```json
   {
       "libmath_ops.so": "<sha256_hash>",
       "libtransform.so": "<sha256_hash>",
       "test_integration.py": "<sha256_hash>"
   }
   ```
3. Start a background python HTTP server (using `http.server`) serving the `/home/user/project/artifacts/` directory on port `8080`. 
4. Write the PID of the background HTTP server process to `/home/user/project/artifacts/server.pid`.

**Constraints:**
- Use standard Python libraries except for `pytest`, which you may need to install (`pip install pytest`).
- Ensure the background process remains running after your script finishes.
You are a QA engineer tasked with dynamically generating a test environment for a microservice architecture. You need to resolve dependency versions, generate build configurations, and compile mock shared libraries to verify the linker configuration.

You have been provided with a file at `/home/user/environment_matrix.json` (which you will need to assume exists, but for the purpose of this task, you should create it with the content described below). 

Here is the exact content you should write to `/home/user/environment_matrix.json` before starting:
```json
{
  "packages": {
    "lib-alpha": {
      "versions": {
        "1.0.0": {},
        "1.1.0": {},
        "1.2.0": {},
        "2.0.0": {}
      }
    },
    "lib-beta": {
      "versions": {
        "1.0.0": { "dependencies": { "lib-alpha": ">=1.0.0,<2.0.0" } },
        "2.0.0": { "dependencies": { "lib-alpha": ">=1.1.0,<2.0.0" } }
      }
    },
    "lib-gamma": {
      "versions": {
        "1.0.0": { "dependencies": { "lib-beta": ">=2.0.0,<3.0.0", "lib-alpha": "<1.2.0" } }
      }
    },
    "test-runner": {
      "versions": {
        "1.0.0": { "dependencies": { "lib-gamma": ">=1.0.0,<2.0.0" } }
      }
    }
  }
}
```

Your task consists of three phases:

**Phase 1: Dependency Resolution (Python)**
Write a Python script `/home/user/resolve.py` that reads `/home/user/environment_matrix.json` and resolves the dependency tree to find the *latest* valid version of each required package to build `test-runner` version `1.0.0`.
- The script must properly parse the semantic version constraints. You may use standard libraries or install packages like `packaging` or `semantic_version` via pip.
- The script must output the final resolved exact versions into `/home/user/resolved_versions.json` as a flat dictionary. E.g., `{"test-runner": "1.0.0", "lib-alpha": "x.y.z", ...}`.

**Phase 2: Source Code Generation**
Using the resolved versions, write a script (or extend your Python script) to generate mock C code in `/home/user/src/`:
- For each dependency (e.g., `lib-alpha`), create a file `lib-alpha.c` containing a single dummy function: `void init_lib_alpha() {}`. Replace hyphens with underscores in the function name.
- For `test-runner`, create a `main.c` that contains a `main()` function which calls the init functions of all other resolved libraries. (Declare the functions using `extern void init_lib_xxx();` at the top of `main.c`).

**Phase 3: Build and Linking**
Write a Makefile or bash script at `/home/user/build.sh` that:
- Creates a directory `/home/user/build/`.
- Compiles each dependency `.c` file into a shared object library (`.so`) in `/home/user/build/`. The output file should be named using the package name and its resolved version, e.g., `lib-alpha-1.1.0.so`. 
- Compiles `main.c` into an executable `/home/user/build/test-runner` that is dynamically linked against all the generated `.so` files.
- Ensure the executable can be run via `./test-runner` from `/home/user/build/` by setting the appropriate rpath or using `LD_LIBRARY_PATH`.

Execute your scripts to generate the JSON, build the C files, and compile the final executable.
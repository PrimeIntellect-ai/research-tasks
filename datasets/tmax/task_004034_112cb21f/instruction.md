You are an engineer working on porting a legacy algorithmic processing tool to run inside a minimal containerized environment. To ensure the tool can be built and tested cleanly from scratch without relying on global system state, you need to create a standalone Continuous Integration (CI) build script.

The tool consists of a C extension that performs algorithmic calculations and a Python wrapper that processes the results.

The source files are located in `/home/user/tool/`:
- `/home/user/tool/src/algo.c`: The core algorithmic logic.
- `/home/user/tool/src/main.py`: A Python script that loads the compiled C library via `ctypes`, calls its functions, and uses third-party Python dependencies to format the output.
- `/home/user/tool/requirements.txt`: The required Python packages for `main.py`.

Your task is to write a Python automation script at `/home/user/tool/ci_build.py` that performs the following CI/CD and build steps:
1. Create a `build` directory at `/home/user/tool/build/`.
2. Compile `/home/user/tool/src/algo.c` into a shared library named `libalgo.so` inside the `build` directory. It must be compiled with position-independent code (`-fPIC`).
3. Create an isolated Python virtual environment at `/home/user/tool/venv/`.
4. Install the dependencies listed in `/home/user/tool/requirements.txt` into this virtual environment.
5. Execute `/home/user/tool/src/main.py` using the Python interpreter from the newly created virtual environment. 
6. **Crucial:** `main.py` expects `libalgo.so` to be available for dynamic linking. Your `ci_build.py` script must execute `main.py` with the `LD_LIBRARY_PATH` environment variable set to include the `/home/user/tool/build/` directory.

If successful, `main.py` will automatically generate a verification file at `/home/user/tool/build/output.txt`.

Ensure your `ci_build.py` script exits with code 0 on success, or a non-zero code if any step fails. You can use standard Python libraries like `os`, `subprocess`, and `sys` to implement this. Do not modify the existing source files.
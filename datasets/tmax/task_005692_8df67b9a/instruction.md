I'm a systems programmer working on a secure token generation web service, and I'm running into a nasty C library linking issue. I have a custom numerical algorithm written in C that is supposed to be wrapped into a Python package for my REST API.

Right now, the Python package won't install correctly because the `setup.py` is broken, and even when I hack it to compile, importing it crashes because it can't find the shared library at runtime.

The code is located in `/home/user/workspace/token_api/`.

Here is what I need you to do:
1. Compile the C source file `src/core_algo.c` into a shared library named `libcorealgo.so` and place it in the `/home/user/workspace/token_api/lib/` directory. (You may need to create the directory).
2. Fix the `setup.py` file so that the Python extension module (`token_ext`) correctly compiles against `libcorealgo.so`. Crucially, you must configure the setup script so that the library is found at *runtime* without needing to manually export `LD_LIBRARY_PATH` (hint: use the correct rpath arguments).
3. Install the Python package in the current environment using `pip install -e .`.
4. Start the REST API server by running `python app.py &`. It will listen on port 8080. Wait a couple of seconds for it to start.
5. Benchmark / test the API by making a single `GET` request to `http://localhost:8080/generate?seed=12` and save the exact raw JSON response to `/home/user/api_output.json`.

Please fix my build setup and get the API successfully returning data!
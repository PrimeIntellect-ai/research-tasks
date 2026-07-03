I have a project in `/home/user/project` that implements a high-performance rate-limiting validator using a C library called via Python `ctypes`. Right now, all files are dumped in a single flat directory, the build system is missing, and the Python FFI bindings are buggy. 

I need you to organize the project files, compile the shared library, fix the FFI bindings, and run the pipeline to generate a final report.

Here are your instructions:
1. **Organize the directory**: Inside `/home/user/project`, create the following directories: `src`, `include`, `lib`, `app`, and `data`.
2. Move the files as follows:
   - `validator.c` -> `src/`
   - `validator.h` -> `include/`
   - `processor.py` -> `app/`
   - `limits.json` and `requests.json` -> `data/`
3. **Build the C library**: Compile `src/validator.c` into a shared library named `libvalidator.so` and place it in the `lib/` directory. Ensure the compiler knows to look for header files in the `include/` directory.
4. **Fix the Python script**: Open `app/processor.py`. It has a few issues:
   - It needs to load the shared library from the new `../lib/libvalidator.so` path (relative to the script's location, or use an absolute path).
   - The `ctypes` argument types and return types for `check_rate_limit` are commented out/missing, causing type errors during the FFI call. Fix them so it passes standard C integers.
   - The script is hardcoded to look for JSON files in its current directory. Update the paths to correctly read from and write to the `../data/` directory.
5. **Run the processor**: Execute the fixed `app/processor.py`. It should read `limits.json` and `requests.json` from the `data` directory, process the rate limits via the C library, and output a validated JSON file to `/home/user/project/data/results.json`.

Please complete these steps. I will verify success by checking the structure of the project and the exact contents of `/home/user/project/data/results.json`.
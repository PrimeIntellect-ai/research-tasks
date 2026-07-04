You have been given a messy Python project that relies on a custom C extension located in `/home/user/project`. 

The project contains the following files:
- `/home/user/project/setup.py`
- `/home/user/project/src/processor.c`
- `/home/user/project/src/helper.c`
- `/home/user/project/include/helper.h`

Your objectives are to organize and fix the project:
1. **Fix the Build System**: The `setup.py` currently fails to build the C extension due to a linking error. You need to fix it so that `python3 setup.py build_ext --inplace` successfully compiles the module `fast_processor`.
2. **Video Analysis**: There is a video file at `/app/glitch.mp4`. Use `ffmpeg` or Python to analyze the video. Count the exact number of frames that are **pure red** (RGB: 255, 0, 0 with no other colors). Let this count be `N`.
3. **Memory Safety Repair**: The C extension has a memory safety vulnerability (buffer overflow / undefined behavior) when processing strings. You must fix the C code (`src/processor.c`). As part of the fix, enforce a strict maximum input length limit equal to `N` (the pure red frame count). If an input string is longer than `N`, safely truncate it to `N` characters before processing, ensuring no buffer overflows occur.
4. **Integration**: Create a Python script at `/home/user/run_processor.py`. This script must import the compiled `fast_processor` module, take a single command-line argument (a string), pass it to `fast_processor.process_string()`, and print the resulting string to standard output. 

Requirements:
- You should use property-based testing (e.g., `hypothesis`) or memory profiling tools (like `valgrind`) to ensure your C extension fix is robust and leak-free.
- The output of `/home/user/run_processor.py <input_string>` must perfectly match the expected behavior: it should safely handle any string, truncate to `N` if necessary, and apply the processing logic originally intended by the C code without crashing.
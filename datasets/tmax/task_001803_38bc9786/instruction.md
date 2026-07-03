You are tasked with debugging a failing build for a custom Python video processing pipeline. The project uses a C-extension to quickly extract specific frames from a video based on metadata, but the build is currently failing, and even when forced to compile, it produces linker errors and runtime crashes.

The project is located in `/workspace/vid_project/`.

Here is the context and your objectives:

1. **Format Parsing Bug (`setup.py` and `libs.conf`)**:
   The `setup.py` script attempts to read linker flags and library dependencies from `/workspace/vid_project/libs.conf`. However, the parsing function `get_libs()` in `setup.py` fails on certain edge cases in the configuration file (e.g., inline comments, trailing whitespace, and multi-line continuation). 
   * Create a minimal reproducible example named `/workspace/vid_project/mre_parse.py` that imports `get_libs` from `setup.py`, parses `libs.conf`, and prints the resulting python list of libraries.
   * Fix the format parsing bug in `setup.py` so that all required libraries (like `avformat`, `avcodec`, `avutil`, `swscale`) are correctly extracted without trailing comments or broken strings.

2. **Compiler and Linker Errors (`extractor.cpp`)**:
   The primary implementation is a C++ PyBind11 extension (`extractor.cpp`) that interfaces with FFmpeg libraries. Once you fix the parsing bug, running `python setup.py build_ext --inplace` will reveal compiler and linker errors. 
   * Diagnose and fix the compiler/linker errors. (Hint: Pay close attention to how C++ includes C headers like FFmpeg's `libavformat`, and ensure the correct linkage block is used).

3. **Video Processing and Integration**:
   Once the extension compiles successfully into an `.so` file, you need to test the pipeline. There is a script `/workspace/vid_project/run_pipeline.py`. 
   Run it against the video fixture located at `/app/test_video.mp4`. 
   The command should be: `python run_pipeline.py /app/test_video.mp4 /workspace/output_frames/`

   This will extract a specific sequence of frames. 

Ensure that all extracted frames are successfully saved in `/workspace/output_frames/` as `.jpg` files. We will verify the correctness of your extracted frames against a reference ground-truth extraction using an automated image similarity metric (SSIM).

Do not modify the core extraction logic in `run_pipeline.py`, only fix the build, the parsing logic, and the extension configuration so that it compiles and runs flawlessly.
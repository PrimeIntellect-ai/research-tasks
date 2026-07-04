You are a QA engineer setting up a test environment for our physics simulation pipeline. We are migrating our trajectory prediction module to C, but the current project is broken. 

You need to complete the following tasks:

1. **Video Analysis**: We lost the original parameters of our physics model. However, we have a calibration video at `/app/calibration.mp4` (640x480 resolution). The video shows a white dot (a few pixels wide) moving on a black background over 100 frames. 
   - Extract the frames and track the center of the white dot.
   - The dot's coordinates `(x, y)` follow an exact integer polynomial trajectory based on the frame index `t` (where `t=0` is the first frame). Determine the equations for `x(t)` and `y(t)`.

2. **Fix the CMake Build**: The C project is located at `/home/user/project`. It consists of a shared library and a main executable. Currently, if you try to build and run it, it fails because CMake cannot link the shared library correctly, and the executable cannot find the shared library at runtime. 
   - Fix the `CMakeLists.txt` so that the project compiles successfully and the executable runs without needing `LD_LIBRARY_PATH` workarounds.

3. **Implement the Predictor**: 
   - Update `traj.c` to implement the function `void get_position(int t, int *x, int *y)`. 
   - Use the mathematical formulas you derived from the video to calculate the `x` and `y` coordinates for any time `t`.
   - The main program `main.c` (already written) reads `t` from the first command-line argument and prints the coordinates as `x y`.

4. **Testing**:
   - Build the executable at `/home/user/project/build/predictor`.
   - The automated verification system will run your compiled executable against thousands of random values of `t` from `0` to `10000` to ensure it is perfectly equivalent to our ground-truth oracle.

Ensure your final executable is located exactly at `/home/user/project/build/predictor`.
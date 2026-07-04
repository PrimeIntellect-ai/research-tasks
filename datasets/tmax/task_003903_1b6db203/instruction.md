You are a mobile build engineer maintaining the testing pipelines for a mobile application. Currently, touch event traces from automated UI tests are filtered using a proprietary, black-box binary (`/app/oracle_smoother`). We need to replace this binary with a highly performant, natively compiled C++ implementation that produces perfectly identical outputs, integrated cleanly into our build system.

Your task is to write the C++ implementation, set up a dynamic build system, and orchestrate the validation process.

**Requirements:**

1. **Video Fixture Analysis:** 
   Our touch tests are recorded. You are provided with a sample video at `/app/touch_recording.mp4`. 
   You must use `ffprobe` (or similar) to determine:
   - The average frame rate (parsed as an integer, e.g., 30 or 60).
   - The total number of frames.

2. **Build System Configuration:**
   Create a `CMakeLists.txt` in `/home/user/` that automatically extracts the frame rate and total frame count from the video *during the CMake configuration step* (using `execute_process`). 
   The build system must pass these two values to your C++ code as preprocessor definitions: `VIDEO_FPS` and `MAX_FRAMES`.

3. **C++ Implementation (`/home/user/smoother.cpp`):**
   Write a C++ program that reads pairs of floating-point numbers (`x` and `y`) from standard input until EOF.
   - It must apply an Exponential Moving Average (EMA) to smooth the trajectory.
   - The smoothing factor $\alpha$ must be computed as: `alpha = 2.0 / (VIDEO_FPS + 1.0)`.
   - The EMA formula is: $S_t = \alpha Y_t + (1 - \alpha) S_{t-1}$. The initial smoothed value is simply the first input value ($S_0 = Y_0$).
   - **Constraint:** If the number of input coordinates read exceeds `MAX_FRAMES`, the program must immediately stop processing inputs and exit.
   - **Output:** Print the smoothed `x` and `y` values to standard output, space-separated, formatted to exactly 4 decimal places, one pair per line.

4. **Integration & Benchmarking:**
   - Compile your project into a `build/` directory so the executable is located at `/home/user/build/smoother`.
   - Write an orchestration script (`/home/user/benchmark.sh`) that generates 100 random floating-point coordinate pairs, runs them through both `/app/oracle_smoother` and `/home/user/build/smoother`, and asserts that the outputs are bit-exact matches. 

The automated verifier will strictly test your compiled `/home/user/build/smoother` binary against the `/app/oracle_smoother` binary using a fuzz-equivalence strategy across thousands of randomized touch streams.
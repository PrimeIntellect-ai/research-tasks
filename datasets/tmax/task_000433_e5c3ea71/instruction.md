You are a performance engineer working on a scientific computation pipeline. Your team analyzes visual telemetry from legacy hardware using a very slow, unoptimized C-based signal filter. Your goal is to extract the test data, establish a reference baseline, and write an optimized, drop-in replacement in Python that produces bit-exact identical output.

**Step 1: Telemetry Extraction**
We have recorded a telemetry trace as a video file located at `/app/telemetry_trace.mp4`. The video is at 30 FPS, and each frame contains a single bright white pixel (255, 255, 255) on a completely black background.
*   Write a script to extract the X-coordinate of this bright pixel for every frame in the video.
*   Save these X-coordinates as space-separated integers in `/home/user/extracted_signal.txt`.

**Step 2: Legacy Source Compilation & Reference Generation**
The legacy C filter is located at `/app/src/legacy_filter.c`. 
*   Compile this source file into an executable at `/home/user/legacy_filter`.
*   The executable reads a single line of space-separated integers from `stdin` and writes the filtered integers to `stdout`.
*   Run your extracted signal through this compiled executable and save the output to `/home/user/reference_output.txt`. This represents your gold-standard reference dataset.

**Step 3: Optimized Python Implementation**
The C implementation is incredibly slow for large datasets because of an $O(N^2)$ windowing bug in its logic. 
*   Analyze the behavior of the C code (or the source code itself) to understand the mathematical filter it applies (it is a rolling max-min difference filter with a specific padding strategy).
*   Write a highly optimized Python script at `/home/user/fast_filter.py` that implements the exact same logic.
*   Your Python script must read a single line of space-separated integers from `stdin`, apply the filter, and print the resulting space-separated integers to `stdout`.
*   It must produce bit-exact equivalent output to `legacy_filter` for any sequence of non-negative integers.

Ensure your Python code handles edge cases exactly as the C code does. An automated fuzzing suite will verify your Python script against thousands of random inputs.
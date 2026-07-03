I'm investigating a long-running video monitoring service that recently started crashing and producing inaccurate anomaly scores. 

We process security footage, extract the average brightness of each frame, and run it through a C++ anomaly detection filter. The filter calculates a sliding window variance over the last 10 frames to detect sudden changes. However, I suspect the C++ filter has a memory leak, an off-by-one error in its window boundary logic, and floating-point numerical instability (precision loss).

Here is what you need to do:
1. Examine the source code of the filter at `/home/user/anomaly_filter.cpp`. 
2. Fix the bugs: resolve the memory leak, correct the off-by-one boundary condition in the sliding window, and upgrade the variance calculation to avoid catastrophic cancellation (e.g., use `double` and a numerically stable algorithm or correct formulas).
3. Compile your fixed program to `/home/user/anomaly_filter`. Your fixed binary must perfectly match the behavior of the proprietary reference binary located at `/app/oracle_filter` for any valid input stream of numbers.
4. Extract the per-frame average brightness from the video file located at `/app/camera_feed.mp4`. (Hint: You can use `ffmpeg` with filters like `showinfo` or `signalstats`).
5. Extract just the mean brightness values (a sequence of numbers), one per line, and pipe them into your fixed `/home/user/anomaly_filter`.
6. Save the final variance output to `/home/user/brightness_anomalies.txt`.

Your final output must be bit-exact equivalent to the oracle when fuzzed with random numerical streams, and your `brightness_anomalies.txt` must contain the exact variance sequence for the provided video.
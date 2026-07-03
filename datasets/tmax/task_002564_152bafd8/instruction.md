You are an MLOps engineer. We suffered a critical data loss of the telemetry logs for our latest object-tracking ML experiment. However, we still have the raw dashboard screen recording of the experiment, located at `/app/experiment_monitor.mp4`.

Your task is to build an ETL and analysis pipeline in **C** to reconstruct the artifact tracking data from this video, aggregate it, and perform hypothesis testing.

**Step 1: Telemetry Extraction (ETL)**
The video is a 640x360 grayscale MP4. In every frame, the tracked ML artifact appears as the single brightest circular spot on a dark background.
Write a C program that reads the raw video frames (you may use `ffmpeg` to decode and pipe raw `gray` frames to your C program's stdin) and extracts the `(x, y)` coordinates of the artifact. You can estimate the coordinates by finding the pixel with the maximum brightness (if there's a tie, pick the first one encountered in row-major order).

**Step 2: Binary Storage Management**
Your C program must store the reconstructed tabular data sequentially into a raw binary file at `/home/user/telemetry.bin`. 
For every frame, write a 12-byte record consisting of:
- `frame_index` (32-bit signed integer, starting at 0)
- `x_coord` (32-bit float)
- `y_coord` (32-bit float)
Ensure there is no padding between records.

**Step 3: Tabular Aggregation & Hypothesis Testing**
We need to know if the artifact's horizontal position significantly drifted between the first half of the experiment and the second half.
Write a second C program (or extend the first) to read `/home/user/telemetry.bin` and compute:
1. The mean `x` coordinate for the first half of the frames (frames `0` to `N/2 - 1`).
2. The mean `x` coordinate for the second half of the frames (frames `N/2` to `N - 1`).
3. Welch's t-test statistic comparing the two halves (assume unequal variances). 

Write these three float values to `/home/user/stats.csv` in the exact format:
`mean_x_first_half,mean_x_second_half,t_statistic`

**Constraints & Verification:**
- You MUST write the processing and mathematical logic in C.
- You may use standard shell tools (like `ffmpeg`) to handle the video container and decode to raw pixel bytes.
- Your output in `telemetry.bin` will be graded based on the Root Mean Square Error (RMSE) against the true artifact coordinates. The RMSE must be less than 2.0 pixels.
You are a data engineer building an ETL pipeline to process optical sensor data stored as video files. 

We have a 24 FPS video file located at `/app/sensor_video.mp4`. Your task is to extract a specific signal from this video and write a Rust program to process it into a clean, normalized time-series dataset.

Perform the following steps:
1. **Feature Extraction**: Extract the average grayscale brightness (luminance) of each frame in the video in temporal order. You may use `ffmpeg` or any standard tool to extract these values.
2. **Resampling**: The original data is 24 FPS. Resample this 1D sequence down to 8 FPS by taking the arithmetic mean of every consecutive block of 3 frames.
3. **Rolling Statistics**: Apply a Simple Moving Average (SMA) with a window size of 4 to the resampled 8 FPS sequence. (The first valid output will occur once you have 4 resampled data points).
4. **Normalization**: Min-max normalize the smoothed sequence so the minimum value becomes 0.0 and the maximum value becomes 1.0.
5. **Output**: Write your processing logic in Rust. The final output must be saved to `/home/user/result.csv` with exactly two columns and a header: `idx,value`. `idx` should be a 0-based integer representing the sequence index of the valid SMA output (starting at 0 for the first valid smoothed point), and `value` is the normalized float value.

You have full access to standard bash utilities and the Rust toolchain (e.g., `cargo`, `rustc`).

Your solution will be evaluated programmatically. The system will compute the Mean Squared Error (MSE) between your `value` column and the perfectly calculated reference truth. To pass, your output's MSE must be less than `0.001`.
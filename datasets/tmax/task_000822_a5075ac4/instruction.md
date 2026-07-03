You are an AI assistant helping a data scientist clean and process a visual dataset using Go.

We have a video file located at `/app/data_feed.mp4`. This video contains simulated telematics data captured via a camera, but the feed is noisy and contains frozen frames. 

Your task is to build a Go-based data processing pipeline that extracts frame-level features, cleans the data, computes rolling statistics, and calculates similarities. You may use `ffmpeg` via shell commands or `os/exec` to extract the frames, but the data processing logic MUST be implemented in Go.

Perform the following steps:
1. **Feature Extraction**: Extract frames from `/app/data_feed.mp4` at exactly 10 frames per second (fps). For each frame (starting at index 0), convert it to 8-bit grayscale and calculate the average pixel intensity (a float value between 0 and 255).
2. **Cleaning & Deduplication**: The camera occasionally freezes. Keep the very first frame (index 0). For all subsequent frames, only keep the frame if its average grayscale intensity differs by strictly greater than `1.0` from the *most recently kept frame*. Discard the others.
3. **Normalization**: Divide the intensity values of the kept frames by `255.0` to normalize them to a `[0.0, 1.0]` range.
4. **Rolling Statistics**: Compute a rolling Simple Moving Average (SMA) of the normalized intensity with a window size of `5`. (For the first 4 kept frames, the SMA is the average of the kept frames seen so far).
5. **Distance Computation**: Calculate the absolute difference between the current frame's SMA and the previous kept frame's SMA. (This value is `0.0` for the first kept frame).

Save the final processed dataset to `/home/user/processed_signal.csv`. The CSV must have a header row and exactly the following columns:
`original_frame_index,normalized_intensity,rolling_sma,sma_diff`

Ensure your Go program is saved and run to produce the final CSV. An automated test will evaluate the accuracy of your `rolling_sma` column against a ground-truth reference using a Mean Squared Error (MSE) metric.
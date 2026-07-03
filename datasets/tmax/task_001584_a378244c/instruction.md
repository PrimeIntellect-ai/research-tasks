You are an ML engineer preparing training data from a video stream. We have a video artifact located at `/app/video.mp4`. 

We need to analyze this video to find frames that are similar to the very first frame, and we must do this efficiently using a custom C program. Additionally, we need to compute the 95% confidence interval for the average brightness across all frames.

Please perform the following steps:
1. Extract all frames from `/app/video.mp4` at 1 frame per second (fps) as JPEG images into `/home/user/frames/`. Use the format `frame_%04d.jpg` (starting at 1 for the first frame, i.e., `frame_0001.jpg` corresponds to 0 seconds).
2. Write a C program, saved as `/home/user/analyze_frames.c`, that reads these JPEG files (you may install and use libjpeg or just extract raw RGB via a quick ffmpeg conversion to a raw binary format like rgb24 before processing, which is recommended to enforce a strict uncompressed binary data schema). 
3. Your C program must compute a simple "embedding" for each frame: a 3-dimensional vector representing the average Red, Green, and Blue channel values for the entire frame.
4. Compute the L2 distance (Euclidean distance) between the embedding of `frame_0001` and all other frames. Find the index of the frame (excluding frame 1) that is most similar to frame 1.
5. Calculate the overall "brightness" of each frame as `(R + G + B) / 3`. Then, assuming the brightness values across all extracted frames follow a normal distribution, compute the 95% confidence interval for the mean brightness.
6. Output your findings to `/home/user/results.json` with the following exact JSON schema:
```json
{
  "most_similar_frame_file": "frame_XXXX.jpg",
  "min_l2_distance": 12.34,
  "brightness_mean": 100.5,
  "brightness_ci_lower": 95.2,
  "brightness_ci_upper": 105.8
}
```

Ensure your C program handles the uncompressed raw binary schema correctly (e.g., 3 bytes per pixel).
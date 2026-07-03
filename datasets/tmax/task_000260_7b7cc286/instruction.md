You have inherited an old, pure-Bash video data processing codebase located in `/home/user/pipeline/`. The previous developer tried to implement a custom video frame analysis tool that calculates an adaptive threshold for frame intensities and outputs a serialized JSON report. 

However, the pipeline is currently broken and produces malformed data, or gets stuck in infinite loops. Your goal is to debug and fix the bash scripts so that they correctly process the provided video at `/app/video.mp4` and output a valid JSON file to `/home/user/output.json`.

Here are the specific issues you need to track down and fix:
1. **Convergence Failure**: `find_threshold.sh` uses an iterative algorithm (similar to ISODATA) to find a threshold for frame intensities. It's supposed to converge when the threshold changes by less than 0.01 between iterations. However, it either exits on the first iteration or loops forever due to a bug in how Bash or `awk` evaluates the convergence condition.
2. **Floating-Point Precision**: `extract_metrics.sh` uses `awk` to calculate the average intensity of frames. There is a precision or rounding bug causing the output to truncate to integers or lose significant digits, drastically reducing the accuracy of the metric.
3. **Encoding and Serialization**: The final output is generated in `serialize.sh`. It extracts the video title metadata using `ffprobe` and constructs a JSON file. The video title contains special characters (quotes, backslashes) that are not being properly escaped, resulting in invalid JSON output.

To complete the task:
1. Fix the scripts in `/home/user/pipeline/`.
2. Run `./process.sh /app/video.mp4 /home/user/output.json`.
3. The final JSON must be perfectly valid and contain an array of `frame_thresholds`. 

Our automated testing suite will parse `/home/user/output.json` and calculate the Mean Squared Error (MSE) between your calculated frame thresholds and the ground truth. Your output must be valid JSON, and the MSE must be less than `0.05`.
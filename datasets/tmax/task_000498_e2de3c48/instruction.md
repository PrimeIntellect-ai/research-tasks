You are an MLOps engineer tasked with processing experiment artifacts from an autonomous driving run and benchmarking inference performance.

We have a dashcam video of an experiment located at `/app/experiment.mp4`, along with vehicle telemetry data in `/app/telemetry.csv`. 
There is a baseline object detection simulation script at `/app/baseline_inference.py`. This script takes a single image path as an argument, performs a heavy CPU-bound mathematical operation (simulating inference), and prints the `filename,object_count,inference_time`.

Your goal is to build an optimized data processing pipeline that extracts frames, runs the inference simulation, and joins the results with the telemetry data.

Here are your instructions:
1. You must create an optimized python script at `/home/user/optimized_pipeline.py` that takes two arguments: `<input_video_path>` and `<output_csv_path>`.
2. When run, your script should:
   a. Extract frames from the input video at exactly 1 frame per second (1 fps). Frame timestamps should be considered 0, 1, 2, etc. based on their second in the video.
   b. Run the exact same inference logic found in `baseline_inference.py` on every extracted frame. You may import functions from `baseline_inference.py` or copy its logic, but the `object_count` for each frame must perfectly match what the baseline script would output.
   c. Optimize the inference execution! The baseline script processes images sequentially. Your script must leverage parallelism (e.g., Python's `multiprocessing`) to achieve a significant speedup. Your pipeline's total execution time (extraction + inference) will be benchmarked against a sequential baseline.
   d. Join the inference results with `/app/telemetry.csv`. The telemetry file contains `timestamp`, `speed`, `lat`, and `lon`. Join the data based on the timestamp (second of the video = telemetry timestamp).
   e. Save the joined data to the `<output_csv_path>`. The output CSV must have the following columns in this exact order: `timestamp,object_count,speed,lat,lon`. The rows should be sorted by `timestamp` ascending.

3. After writing your script, run it to process `/app/experiment.mp4` and save the output to `/home/user/merged_results.csv`.

Requirements:
- Ensure all required packages (like `pandas`, `numpy`, `opencv-python-headless` or `ffmpeg-python`) are installed as needed in your environment. `ffmpeg` is available on the system.
- Do not alter the mathematical logic used to compute `object_count`.
- Your code must be robust enough to be tested by our automated verifier, which will run `/home/user/optimized_pipeline.py` on a hidden test video to measure the speedup metric.
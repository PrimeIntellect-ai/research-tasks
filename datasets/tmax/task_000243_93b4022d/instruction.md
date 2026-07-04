My CI build is failing during the video preprocessing stage. Our pipeline script at `/home/user/video_processor.py` is supposed to extract frame timestamps from an input video, but it's currently crashing with a `RecursionError`. Even when we try to bump the recursion limit, the output timestamps drift significantly due to floating-point precision issues, causing our downstream frame-extraction (using `ffmpeg`) to fail or grab the wrong frames.

The script processes a test video located at `/app/test_video.mp4`. It is supposed to generate exactly 5.0 seconds worth of timestamps at 30 frames per second, starting from 0.0 up to (but not including) 5.0. 

Your tasks are:
1. Debug `/home/user/video_processor.py` to identify why the recursion fails and why the floating-point accumulation causes drift.
2. Refactor the `get_timestamps` function to use a standard loop instead of recursion.
3. Fix the floating-point precision issue so that the timestamps do not drift (hint: multiply and divide by integer frame indices rather than accumulating floats).
4. Run your fixed script. It should write the corrected timestamps as a JSON list of floats to `/home/user/fixed_timestamps.json`.

Ensure your code is precise. Our automated evaluation will measure the Mean Squared Error (MSE) between your output timestamps and the mathematically ideal timestamps, expecting the error to be virtually zero.
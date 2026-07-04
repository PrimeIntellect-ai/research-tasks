You are an engineer tasked with investigating and fixing a buggy, long-running video processing service. 

We have a Python script located at `/app/video_processor.py` that extracts frames from a video, performs some basic analysis (calculating the average pixel intensity per frame), and serializes the results to a custom binary format. 

However, the script has two major issues:
1. It has a severe memory leak that causes it to crash when processing long videos.
2. The shell wrapper `/app/run_processor.sh` and the Python script itself fail to properly handle video files that have spaces in their filenames. This results in encoding and serialization errors.

Your objective is to:
1. Debug and fix the memory leak in `/app/video_processor.py` (which uses OpenCV and stores raw frame data unnecessarily).
2. Fix the filename parsing bug in both `/app/run_processor.sh` and `/app/video_processor.py`.
3. Output the fully fixed Python script to `/app/video_processor_fixed.py`.

The fixed Python script must take exactly two arguments: the input video path and the output binary file path. 
For example: `python3 /app/video_processor_fixed.py "/app/test videos/sample 1.mp4" /tmp/output.bin`

A sample video is provided at `/app/sample videos/test leak.mp4` for you to test your fixes. 
The output binary format must remain exactly the same as intended by the original script: a 4-byte integer (little-endian) representing the number of frames, followed by N 4-byte floats (little-endian) representing the average intensity of each frame.

We will verify your solution by running it against a suite of randomly generated test videos and comparing its output bit-for-bit against a reference implementation.
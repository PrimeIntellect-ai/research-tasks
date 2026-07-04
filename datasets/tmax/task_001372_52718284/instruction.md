You are tasked with migrating a legacy Python 2 script to Python 3. The script acts as a simulated REST API backend that processes video frames and performs a simple image analysis.

In your environment, there is a video file located at `/app/video.mp4`.
You will also find a legacy Python 2 script at `/home/user/legacy_api.py`. This script takes a single integer argument representing a frame number, extracts that specific frame from the video using `ffmpeg` (as a grayscale PGM image), counts the number of "bright" pixels (value > 128), and outputs a JSON response with the result.

However, `/home/user/legacy_api.py` is written in Python 2 and fails to run in your current Python 3 environment (it contains `print` statements without parentheses, uses `xrange`, and relies on Python 2 integer division semantics that must be carefully translated). 

Your task is to:
1. Analyze the logic in `/home/user/legacy_api.py`.
2. Write a fully compatible Python 3 version of the script and save it to `/home/user/api_v3.py`.
3. Ensure `/home/user/api_v3.py` takes a frame number as its first CLI argument and prints exactly the same JSON string to standard output as the original script would have. The JSON format must strictly be `{"frame": <N>, "bright_pixels": <count>}`.
4. Your script must efficiently extract only the requested frame using `ffmpeg`.

To verify your work, an automated fuzzer will run your script `/home/user/api_v3.py` against a known reference binary for 20 random frame numbers between 0 and 300, and assert that the outputs match exactly.
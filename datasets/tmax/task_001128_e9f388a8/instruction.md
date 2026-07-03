You are tasked with building a polyglot video analysis tool from scratch in Bash, C, and Python. The goal is to create a pipeline that extracts frames from a video, detects scene changes by computing the Mean Squared Error (MSE) between consecutive frames using a custom C library via Python FFI, and orchestrates everything with Bash.

Here are the requirements for the system:

1. **`build.sh` (Bash)**
   Write a script at `/home/user/build.sh` that compiles a C library. It should output a shared library named `libdetector.so` in `/home/user/`. Include any necessary compiler flags for creating a shared library.

2. **`detector.c` (C)**
   Write the C source code at `/home/user/detector.c`. It must export a function:
   `double compute_mse(const unsigned char* frame1, const unsigned char* frame2, int size)`
   This function calculates the Mean Squared Error between two raw 8-bit byte arrays (RGB24 pixels) of length `size`.

3. **`wrapper.py` (Python)**
   Write a Python script at `/home/user/wrapper.py` that uses `ctypes` to load `/home/user/libdetector.so`. 
   It should accept command-line arguments: `python3 wrapper.py <file1.raw> <file2.raw> <size_in_bytes>`.
   It must read the binary data from the two raw frame files, pass them to `compute_mse`, and print the resulting MSE as a float to stdout.

4. **`analyze.sh` (Bash)**
   Write the main orchestrator at `/home/user/analyze.sh`. 
   It must accept a single URI argument in the format: `vidproc://<absolute_video_path>?width=<w>&height=<h>&fps=<f>`
   (e.g., `vidproc:///app/test_video.mp4?width=320&height=240&fps=5`).
   
   The script must:
   - Parse the URI to extract the file path, width, height, and fps.
   - Use `ffmpeg` to extract raw RGB24 frames from the video at the specified fps and resolution into a temporary directory. (Name the frames sequentially, e.g., `frame_0001.raw`).
   - Iterate through consecutive frame pairs.
   - Call `wrapper.py` for each pair.
   - Sort the results to find the transitions with the highest MSE.
   - Save the raw output of all frame pairs and their MSE to `/home/user/mse_log.txt` in the format `frame_N.raw frame_N+1.raw <MSE>`.

There is a test video located at `/app/test_video.mp4` that you can use to test your pipeline. 

Ensure all scripts are executable. Your solution will be tested by an automated grading script that evaluates the mathematical accuracy of your MSE implementation against a hidden benchmark.
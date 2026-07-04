You are a release manager preparing a deployment for our new automated video processing pipeline. The development team has dropped a messy bundle of files in `/home/user/video_toolkit` and asked you to finalize the build and deployment scripts. 

You must orchestrate a Bash-only pipeline that extracts frames from a provided video, rate-limits the processing, and validates the toolset. 

Here are your specific objectives:

1. **Build and Shared Library Management**:
   In `/home/user/video_toolkit`, there is a C source file `frame_processor.c` and two pre-compiled shared libraries: `libprocess_v1.so` (unoptimized) and `libprocess_v2_opt.so` (optimized with new ABI). 
   Write a Bash script `/home/user/video_toolkit/build.sh` that compiles `frame_processor.c` into an executable named `processor`. You must ensure that `processor` is dynamically linked and correctly uses the optimized `libprocess_v2_opt.so` at runtime. The developer noted that `libprocess_v2_opt.so` has a slightly different ABI version for the `process_frame` symbol. You must resolve any runtime linking issues (e.g., using `LD_LIBRARY_PATH` or `LD_PRELOAD` in your wrapper) so that running `./processor` executes the optimized code.

2. **Request Validation and Rate Limiting**:
   Write the main pipeline script at `/home/user/pipeline.sh`. This script must:
   - Accept a video file path as its first argument.
   - Validate that the file exists and is a valid MP4 (use `ffprobe` or standard tools; exit code 1 if invalid).
   - Extract the first 50 frames of the video as JPEG images to `/home/user/frames/` using `ffmpeg` (e.g., `frame_01.jpg`, `frame_02.jpg`, etc.). A sample video is provided at `/app/traffic.mp4`.
   - Iterate through these extracted frames and pass each one to the `processor` executable. 
   - **Rate Limiting**: Our downstream storage API (simulated by the `processor` tool) crashes if it receives too many requests. Your Bash script MUST rate-limit the execution of `processor` to exactly 5 frames per second. 
   - Append the stdout of each `processor` run to `/home/user/processing.log`.

3. **Property-Based Testing**:
   The `processor` binary is known to segfault on malformed files. Write a Bash script `/home/user/prop_test.sh` that performs property-based testing on the executable.
   - It should generate 100 random binary files (varying randomly in size between 1KB and 50KB) using `dd` and `/dev/urandom`.
   - Pass each generated file to the `processor`.
   - Count how many times the `processor` exits with a segmentation fault (exit code 139) versus success (exit code 0).
   - Output a single line to `/home/user/test_report.txt` in the format: `Success: X, Segfaults: Y`.

Complete these scripts and ensure `/home/user/pipeline.sh /app/traffic.mp4` runs successfully, respects the 5 FPS rate limit, and generates the correct log file. The final performance of your pipeline will be evaluated by an automated metric threshold verifier measuring the CPU execution time.
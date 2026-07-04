You are a release manager preparing for a critical production deployment. As part of our deployment pipeline, an automated UI test generates a video recording of the deployment progress screen. We need to verify that the deployment succeeded by detecting "success frames" (frames that turn entirely solid red due to our specific test harness signaling) in the recording.

We have a custom C utility located at `/home/user/src/analyze_frame.c` that was written to read raw RGB24 pixel data from standard input, load it into a custom block-based image data structure, and calculate the average red channel intensity to identify success frames. However, the current C implementation is buggy: it consistently segfaults on standard 1080p frames due to memory safety issues (specifically, buffer overflows and undefined behavior in how the custom data structure is allocated and freed).

Your tasks are:
1. **Debug and Repair:** Fix the memory safety issues and undefined behavior in `/home/user/src/analyze_frame.c`. Ensure it compiles without warnings using `gcc -O2`.
2. **End-to-End Orchestration:** Write a Bash script at `/home/user/run_e2e.sh` that orchestrates the entire validation pipeline. The script must:
   - Use `ffmpeg` to extract the raw `rgb24` frame stream from the deployment recording located at `/app/deploy_recording.mp4`.
   - Pipe the uncompressed frame data into the repaired `analyze_frame` utility.
   - Count the total number of "success frames" (where the average red intensity reported by the C tool exceeds 200).
   - Write the final integer count of success frames to `/home/user/result.txt`.
3. **Property-Based Verification:** Inside your Bash script, include a brief setup phase before processing the video that generates random 1920x1080 binary data (e.g., using `/dev/urandom`) and pipes it to the compiled C program for 5 iterations to ensure it no longer crashes on random fuzz input. If the C program crashes during this test, the Bash script should exit with an error.

The final output we will check is the numerical value inside `/home/user/result.txt`. Focus on correct Bash scripting for the orchestration and robust memory fixes for the C code.
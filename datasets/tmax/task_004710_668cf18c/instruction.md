You are an operations engineer tasked with triaging a severe production incident. Our video processing microservice crashed last night, resulting in dropped events and corrupted outputs. 

We have isolated the input that caused the crash to a specific video clip, provided at `/app/incident-stream.mp4`. 
Additionally, we have collected the container logs from the time of the crash in `/app/logs/container.log`.

The source code for the C++ application is located in a Git repository at `/home/user/video_service`. The current `HEAD` of the `main` branch is crashing, but the operations team noted that the release tagged `v1.0.0` was perfectly stable.

Your task consists of the following steps:
1. **Log Timeline Reconstruction & Frame Extraction:** Analyze `/app/logs/container.log` to determine the exact arguments and frame index that caused the crash. Extract the frames from `/app/incident-stream.mp4` using `ffmpeg` (e.g., as raw RGB or grayscale binaries, based on what the log indicates the service was doing).
2. **Git Bisection:** Use the provided Git repository to bisect the regression between `v1.0.0` (good) and `HEAD` (bad). Identify the specific commit that introduced the memory corruption/crash.
3. **Core Dump / Stack Trace Analysis:** Reproduce the crash using the extracted frame to generate a stack trace or core dump, identifying the exact line of code and logic error in the C++ application. 
4. **Fix and Compile:** Fix the bug in the C++ source code. The bug involves an unsafe memory operation introduced during a recent "optimization" commit. 
5. **Integration:** Compile your fixed C++ program. Name the compiled executable exactly `/home/user/fixed_processor`. 

The executable `/home/user/fixed_processor` must behave exactly like the original intended design: it takes a single command-line argument (the path to a raw binary frame file) and writes the processed binary data directly to standard output (`stdout`).

Our automated verification system will extensively test your compiled `/home/user/fixed_processor` against thousands of mutated raw frame files to ensure no further regressions or memory safety issues exist, and that its output perfectly matches our reference implementation.
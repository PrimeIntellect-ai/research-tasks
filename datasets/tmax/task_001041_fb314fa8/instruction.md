You are a security researcher analyzing a suspicious application that processes video files. We have an in-house C++ tool, `video_processor`, which extracts frames from MP4 files to compute analytics. Recently, it crashed while processing a suspicious video (`/app/incident_001.mp4`), leaving behind a core dump at `/home/user/core`. We suspect an adversary crafted a specific video payload to trigger a zero-day in our analytics pipeline.

Your tasks are:
1. **Build Repair:** The source code for `video_processor` is located in `/home/user/src/`. It currently fails to build due to a missing header and a conflicting dependency in the `Makefile`. Fix the build issues and successfully compile `video_processor`.
2. **Core Dump Analysis:** Use `gdb` to analyze the provided `/home/user/core` file. Inspect the stack trace, the local variables, and the source code of `video_processor.cpp` to understand exactly what properties of a video frame cause the application to crash.
3. **Detector Implementation:** Write a standalone C++ program at `/home/user/detector.cpp` and compile it to the executable `/home/user/detector`. 
   - The detector must take exactly one command-line argument: the absolute path to an MP4 video file.
   - It must analyze the video frames (you may use `ffmpeg` or `ffprobe` via `popen` to extract raw frame data).
   - It must identify whether the video contains the malicious payload that caused the crash. 
   - If the video is malicious (contains the crash-inducing frame pattern), it MUST print `REJECT` to `stdout`.
   - If the video is benign, it MUST print `ACCEPT` to `stdout`.
   - The output must be exactly `REJECT` or `ACCEPT` (with an optional newline).

We have provided a few sample files in `/home/user/samples/` for you to test against. 

Your detector will be tested against a hidden, much larger adversarial corpus of videos. It must flawlessly preserve all clean videos and reject all malicious ones.
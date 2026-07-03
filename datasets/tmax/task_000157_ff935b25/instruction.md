You are a systems programmer debugging an infrastructure issue for our video processing pipeline. Our system relies on a custom C library (`libframemeta.so`) linked against an error-correction library (`libecc.so`) to validate and process frame metadata. Recently, the pipeline has been failing.

Your objective is to fix the underlying library issues, build a Bash wrapper to process a specific reference video, and deploy a robust validation filter behind a reverse proxy.

**Step 1: Fix the C Library Linking and Memory Safety**
In `/home/user/workspace/src/`, you will find the source code for the C libraries. 
Currently, the build fails due to a linking issue with `libecc`. Additionally, `libframemeta` contains a critical undefined behavior (buffer overflow) when parsing certain malicious metadata headers.
1. Fix the `Makefile` and source code so that `libframemeta.so` and `libecc.so` compile and link correctly.
2. Patch the memory safety vulnerability in `extractor.c`.

**Step 2: Video Frame Extraction**
We have provided a reference video artifact at exactly `/app/reference_video.mp4`.
Write a Bash script at `/home/user/extract_reference.sh` that uses `ffmpeg` to extract exactly frame 42 from `/app/reference_video.mp4`, passes it through `libframemeta`'s CLI tool (`/home/user/workspace/bin/fm_tool`), and outputs the calculated checksum to `/home/user/frame42_checksum.txt`.

**Step 3: Build an Adversarial Payload Detector**
To protect our backend, you must write a Bash-based filter at `/home/user/detector.sh`. This script takes a single file path as an argument.
- It must analyze the file using your fixed `fm_tool` and pure Bash logic.
- It must exit with code `0` if the payload is safe/clean.
- It must exit with code `1` (or higher) if the payload is malicious/corrupt (i.e., triggers the now-fixed buffer constraints or fails the `libecc` checksum validation).

**Step 4: Reverse Proxy Integration**
Set up an Nginx reverse proxy on port `8080` (running locally). Configure it to proxy requests to a lightweight Bash-based TCP server (which you must write at `/home/user/server.sh`) running on port `9000`. The server should receive a payload via HTTP POST, pass it to your `/home/user/detector.sh`, and return `200 OK` for clean payloads or `400 Bad Request` for evil payloads.

Ensure all services (Nginx, and your Bash server) are running in the background when you finish.
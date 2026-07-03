You are a systems programmer tasked with fixing a broken build and setting up a minimal E2E testing service for a video analysis pipeline.

Currently, we have a C-based analysis tool that is failing to link against a custom shared library. You need to fix the build, extract frames from a test video, and orchestrate a minimal HTTP service in Bash to serve the analysis results.

Here are the specific requirements:

1. **Fix the C Linking Issue:**
   - The source code is in `/home/user/src/`. 
   - `build.sh` is supposed to compile `analyzer.c` and link it against `libcore.so` (located in `/home/user/src/lib/`).
   - The compiled binary should be created at `/home/user/src/analyzer`.
   - Fix `/home/user/src/build.sh` so that it successfully compiles the executable. The executable must be able to run without throwing shared object loading errors (e.g., ensure `LD_LIBRARY_PATH` or rpath is handled correctly during execution or compilation).

2. **Extract Video Frames:**
   - We have a test video located at `/app/test_stream.mp4`.
   - Use `ffmpeg` to extract the first 30 frames of this video into the directory `/home/user/frames/`.
   - The frames must be named exactly `frame_01.png`, `frame_02.png`, ..., `frame_30.png` (1-indexed, zero-padded to 2 digits).

3. **Create the E2E Bash API (HTTP):**
   - Write a Bash script at `/home/user/server.sh` that acts as a simple HTTP server listening on `127.0.0.1:8080`.
   - You may use `nc` (netcat) or `socat` to handle the TCP connections.
   - The server must accept `GET /analyze?frame=<N> HTTP/1.1` requests (where `<N>` is a 2-digit number like `05` or `12`).
   - When a request is received, the script should invoke the compiled C binary on the corresponding frame: `/home/user/src/analyzer /home/user/frames/frame_<N>.png`.
   - The server must respond with a valid HTTP 200 response. The body of the response must be the exact stdout output of the `analyzer` binary.
   - Example Response format:
     ```
     HTTP/1.1 200 OK
     Content-Type: text/plain
     Content-Length: <length>
     
     <output from analyzer>
     ```
   - Run your server in the background so it is listening when your final command completes.

Make sure your `server.sh` is running and bound to port 8080 before you finish.
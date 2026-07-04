You are acting as a performance engineer and forensic investigator. We have a legacy C++ video analytics service located at `/home/user/video_service`. This service is designed to process video files, identify specific "blackout" frames (where average pixel brightness is strictly less than 10), and serve the results over a dual-port network interface. 

Currently, the service is non-functional, and you must diagnose and fix several issues to get it running and correctly analyzing the provided evidence video at `/app/evidence.mp4`.

Here is what you need to do:

1. **Dependency Resolution**: The build system is broken. `CMakeLists.txt` is incorrectly configured to link against a broken, stubbed version of `libavcodec` located in `/home/user/video_service/vendor/` instead of the system-installed FFmpeg libraries. Fix the CMake configuration to use the system libraries so the project compiles successfully.
2. **Secret Recovery**: The service requires an `AUTH_TOKEN` in its `config.ini` file to start up. The token was accidentally deleted from the current working tree, but it was committed at some point in the local git repository history. Recover the token and place it in `/home/user/video_service/config.ini` in the format `AUTH_TOKEN=your_recovered_token`.
3. **Corrupted Input / Boundary Condition Fix**: The custom frame extraction loop in `src/analyzer.cpp` crashes with a segmentation fault when reading to the end of a video file. There is an off-by-one boundary error, and it also fails to gracefully handle a corrupted frame marker injected near the end of `/app/evidence.mp4`. Modify the C++ code to gracefully skip the corrupted frame and fix the loop bounds so it completes the analysis without crashing.
4. **Performance Debugging**: Even if it doesn't crash, the frame processing is currently incredibly slow. Use profiling tools (like `perf` or `gprof`) or inspect the code to find the bottleneck in `src/analyzer.cpp`. There is an egregiously inefficient pixel-copying routine that is strictly O(N^2) instead of O(N) or contains an artificial delay. Optimize it so the entire video processes in under 5 seconds.
5. **Run the Service**: Once fixed and compiled (using `make` inside a `build` directory), run the server binary. It will automatically bind to `127.0.0.1:9000` (HTTP status port) and `127.0.0.1:9001` (TCP analysis port). 

Leave the server running in the background. An automated verifier will:
- Send an HTTP `GET /status` to port 9000 using the recovered `AUTH_TOKEN` in the `Authorization: Bearer <TOKEN>` header.
- Connect to the TCP socket on port 9001 and send the command `ANALYZE /app/evidence.mp4\n`. It expects the service to reply with `FRAMES:[comma_separated_list_of_blackout_frame_indices]\n`.

Do not change the network binding or protocol logic in `src/server.cpp`—only fix the build, the bugs in `src/analyzer.cpp`, the configuration, and then leave the server running.
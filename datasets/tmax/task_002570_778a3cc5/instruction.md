You are a release manager preparing the deployment of a new video analytics microservice. We are migrating our core video motion analysis algorithm from Python to C for performance reasons. However, the migration is incomplete. 

In `/home/user/service/`, you will find a partially implemented project. Your task is to complete the migration, fix the build, resolve memory issues, and bring up the service.

Here is what you need to do:
1. **Understand the Algorithm**: Read `reference.py` to understand the motion analysis algorithm. It reads a video, converts it to 8-bit grayscale (using ffmpeg), and calculates the sum of absolute pixel differences between consecutive frames. It returns the 1-based index of the frame that has the maximum difference from its preceding frame.
2. **Implement and Fix the C Code**: The file `analyzer.c` contains a buggy skeleton of this algorithm. It has compilation errors, logic gaps (you need to translate the core math from the Python reference), and a severe memory leak that will cause it to crash under load. Fix `analyzer.c` so it perfectly replicates the logic of `reference.py` without leaking memory.
3. **Repair the Build System**: The `Makefile` is broken. It fails to compile the C code into a shared library (`libanalyzer.so`) because it is missing the correct compiler flags for position-independent code and shared libraries. Fix the `Makefile` so that running `make` successfully produces `libanalyzer.so`.
4. **Deploy the Service**: We have a Python wrapper `server.py` that loads `libanalyzer.so` via `ctypes` and exposes it over HTTP. 
   - Ensure the server runs and listens on `127.0.0.1:8080`.
   - The server has an endpoint `GET /api/peak_motion` that expects a header `Authorization: Bearer deploy_token_2024`.
   - The server will pass the path of our test video, located at `/app/video.mp4`, to your C library.
   - The endpoint must return a JSON response: `{"peak_frame": <int>}`.

Leave the service running in the background listening on port 8080 when you are finished.
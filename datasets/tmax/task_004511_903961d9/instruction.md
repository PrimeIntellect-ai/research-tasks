You are a developer tasked with organizing a messy video processing project and optimizing its core pipeline. The project extracts frames from a video, calculates the average brightness of each frame, and sends a webhook to an external reporting API. 

Currently, the project is a mess in `/home/user/project/`, and the pure Python implementation is far too slow. A previous developer started writing a Rust extension (using PyO3) to speed up the frame analysis, but it fails to compile due to ownership and borrow checker errors. Furthermore, the CI test pipeline is missing a reverse proxy to mock the external API.

Your tasks are:

1. **Project Organization:**
   Reorganize the `/home/user/project/` directory into the following structure:
   - `/home/user/project/src/` (contains the Python app)
   - `/home/user/project/src/rust_ext/` (contains the Cargo project for the Rust extension)
   - `/home/user/project/tests/` (contains test fixtures and mock servers)

2. **Rust Optimization & Debugging:**
   In `/home/user/project/src/rust_ext/src/lib.rs`, there is a function `calculate_brightness` that takes a flattened byte array of RGB pixels and calculates the average brightness (treating R, G, B equally). 
   - Fix the borrow checker and ownership errors in the Rust code.
   - Build the Rust extension as a Python module named `fast_video_utils` and make it accessible to the Python scripts.

3. **Reverse Proxy and Test Fixture Setup:**
   - Create a mock API server in Python at `/home/user/project/tests/mock_api.py` that listens on port `9090` and accepts POST requests to `/report`. It should log the received JSON to `/home/user/project/tests/api_log.json`.
   - Create a lightweight reverse proxy script `/home/user/project/tests/proxy.py` that listens on port `8080` and forwards all requests to `http://localhost:9090`.

4. **Integration & Refinement:**
   - Update the main application script `/home/user/project/src/process_video.py` to process the video fixture located at `/app/video.mp4`.
   - The script must use `ffmpeg` (or `cv2` if installed) to extract frames, pass the frame data to the Rust `fast_video_utils.calculate_brightness` function, and send a JSON array of the brightness values to `http://localhost:8080/report`.
   - The JSON payload should look like: `{"video": "/app/video.mp4", "frames_brightness": [45.2, 46.1, ...]}`

5. **CI/CD Script:**
   - Write a bash script `/home/user/project/run_ci.sh` that automatically:
     1. Starts the mock API and reverse proxy in the background.
     2. Runs `process_video.py`.
     3. Gracefully shuts down the background processes.
     4. Exits with 0 if successful.

The final evaluation will measure the execution time of your optimized pipeline against a pure Python reference. You must achieve a substantial speedup while maintaining the exact same brightness calculations.
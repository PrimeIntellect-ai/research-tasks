I am a developer trying to organize my project files for a mathematical video analysis application, and I need your help to fix my build and deployment pipeline.

We have a video of a physics experiment located at `/app/pendulum_experiment.mp4`. 
Here are your objectives:

1. **Video Frame Extraction & Organization**:
   Extract all frames from `/app/pendulum_experiment.mp4` at exactly 5 frames per second using `ffmpeg`. Save them as JPEG files in `/home/user/project/frames_raw/` with the format `frame_XXXX.jpg` (1-indexed, padded to 4 digits).
   Write a shell script that organizes these files into `/home/user/project/frames/even/` and `/home/user/project/frames/odd/` based on whether the frame number is mathematically even or odd.

2. **Rust Debugging & Package Management**:
   I have a mathematical processing tool written in Rust located at `/home/user/project/math_filter/`. It computes a custom recursive series used for signal processing (a modified discrete Lyapunov exponent calculation). 
   Currently, it fails to compile due to several Rust ownership and borrow checker errors. Fix the `src/main.rs` file so that it compiles perfectly without altering the mathematical logic or the expected input/output format. The tool expects space-separated floating-point numbers via standard input and prints the computed mathematical hash to standard output.

3. **Cross-Compilation**:
   Update the Rust project's configuration to cross-compile the executable. You must generate two binaries:
   - A native Linux binary placed at `/home/user/project/bin/math_filter_native`
   - A WebAssembly (WASI) module placed at `/home/user/project/bin/math_filter.wasm`

4. **Reverse Proxy Configuration**:
   Install and configure `nginx` to act as a reverse proxy. It must listen on port 8080.
   - Requests to `http://127.0.0.1:8080/assets/even/` should serve the organized even frames.
   - Requests to `http://127.0.0.1:8080/assets/odd/` should serve the organized odd frames.
   Ensure `nginx` is running in the background and serving the files correctly from the organized directories.

Ensure all file paths are exact, and the final compiled Rust binaries exist at the precise locations specified.
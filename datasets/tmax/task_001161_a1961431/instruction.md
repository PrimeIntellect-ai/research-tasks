You are a developer working on a polyglot system that includes a video processing pipeline, a Python HTTP API, and a Rust-based bytecode emulator. 

Currently, the multi-file Rust project located at `/home/user/rust_emulator` fails to compile due to some type and borrowing errors in the interpreter module. 

Your tasks are:
1. **Fix the Rust Project**: Inspect the Rust code in `/home/user/rust_emulator` and fix the compilation errors. The Rust application is a local TCP server listening on `127.0.0.1:9000` that evaluates simple math string commands (e.g., `ADD 10 5`, `MUL 3 4`) and returns the integer result.
2. **Analyze the Video**: There is a video artifact located at `/app/demo.mp4`. Write a Python script to precisely count the total number of frames in this video. You can use `ffmpeg` or `ffprobe`, which are preinstalled.
3. **Create a Python API Server**: Write a Python HTTP server using `Flask` or `FastAPI` (you can install them via pip) that listens on `0.0.0.0:8000`. This server must have two endpoints:
   - `GET /status`: Returns a JSON response containing the frame count of the video, exactly like this: `{"frames": <FRAME_COUNT>}`.
   - `POST /execute`: Accepts a JSON payload like `{"command": "ADD 5 3"}`. It should connect to the Rust TCP server on port 9000, send the command string (with a newline `\n` at the end), read the response, and return it as JSON: `{"result": <INTEGER_RESULT>}`.
4. **Orchestration**: Create a script `/home/user/run.sh` that builds the Rust project in release mode, starts the Rust TCP server in the background, and then starts your Python HTTP server.

Please ensure that by the time you finish, both the Rust emulator and the Python API are running, with the Python API listening on port 8000.
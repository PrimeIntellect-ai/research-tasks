You are an open-source maintainer reviewing a broken Pull Request for a project called `AudioStreamer`. The PR introduces a real-time audio filtering pipeline, but the CI build is failing and the author left some components in Python that need to be rewritten in Bash.

The repository is located at `/home/user/AudioStreamer`. 

Your objectives to merge this PR successfully are:

1. **Fix the Build (CMake & Rust FFI):**
   The project has a C-based audio filter built with CMake in `/home/user/AudioStreamer/c_filter`. It outputs a shared library (`libaudiofilter.so`). 
   The Rust backend in `/home/user/AudioStreamer/rust_server` is supposed to link against this library and expose a WebSocket endpoint. However, the Rust build currently fails to link the C library, and it crashes at runtime if it can't find it. Fix the CMake configuration, `build.rs`, and any environment paths required so that `cargo build --release` succeeds and the binary can run.

2. **Fix Rust Ownership Errors:**
   The PR author wrote the WebSocket server in Rust, but it currently fails to compile due to borrow checker and ownership errors in `src/main.rs`. Debug and resolve these errors. The server must compile and successfully bind to `127.0.0.1:8080`.

3. **Code Translation & Rate Limiting (Bash):**
   The PR includes a Python script `client_chunker.py` that reads an audio file, applies request validation, rate-limits the data transfer to 50 KB/s, and pipes it to the WebSocket server. 
   You must completely rewrite this logic into a Bash script located at `/home/user/AudioStreamer/process_stream.sh`. 
   The Bash script must:
   - Accept an input file as its first argument.
   - Validate the file exists.
   - Read the file and stream it to `localhost:8080` (using `websocat`, `nc`, or similar standard tools) strictly rate-limited to 50 KB per second.
   - Output the server's response to `/home/user/processed_output.wav`.

4. **Integration & Final Output:**
   There is a test audio fixture located at `/app/test_audio.wav`. 
   Start your compiled Rust server in the background. Then, run your Bash script: 
   `bash /home/user/AudioStreamer/process_stream.sh /app/test_audio.wav`
   
   Ensure the final processed audio is completely downloaded and saved exactly at `/home/user/processed_output.wav`. You can use any standard Linux tools or diffing utilities to verify the integrity of the stream compared to direct file processing.
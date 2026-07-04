You are a mobile build engineer maintaining a polyglot data pipeline for a secure communications app. We have a local WebSocket server written in Rust that acts as a local proxy to process audio streams. It uses a highly optimized C library for audio de-obfuscation via FFI.

Unfortunately, the Rust project is currently failing to compile due to lifetime issues and incorrect FFI buffer handling. Furthermore, the build orchestration is broken.

Your tasks:
1. Fix the compilation errors in the Rust project located at `/home/user/ws_proxy/`. The server must compile and successfully link against the C library `libfilter.so` (source located at `/home/user/ws_proxy/c_src/filter.c`).
2. Write a bash script `/home/user/ws_proxy/build.sh` that compiles the C code into a shared library, sets up the necessary environment variables (like `LD_LIBRARY_PATH`), and builds the Rust project.
3. Start the Rust WebSocket server (which binds to `127.0.0.1:8080`).
4. We have an intercepted, obfuscated audio transmission at `/app/intercepted_comms.wav`. A Python client `/home/user/client.py` is provided. Run the Python client to stream `/app/intercepted_comms.wav` through your fixed WebSocket server. The client will automatically save the de-obfuscated result to `/home/user/clear_audio.wav`.
5. Transcribe the contents of `/home/user/clear_audio.wav` and save the exact spoken text to `/home/user/transcript.txt`. You may use `ffmpeg` and any installed local transcription tools (like whisper.cpp, which is available in the environment) to recover the spoken content. 

The primary goal is the successful extraction of the transcript. Ensure your build pipeline is robust and all cross-language memory is handled safely without leaks or panics.
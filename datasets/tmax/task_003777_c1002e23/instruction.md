You are acting as a systems programmer to fix a broken polyglot project and expose its numerical backend via a WebSocket interface. 

We have a C library that performs a high-performance mathematical signal transformation. However, the Makefile is currently broken (it suffers from linking errors and incorrect compiler flags for creating a shared object). 

Furthermore, the calibration parameters for the algorithm were provided to us as an audio voice memo by the lead researcher, located at `/app/calibration.wav`.

Your tasks:
1. **Fix the C build**: Inspect and fix `/app/Makefile` so that running `make` successfully produces `libcore.so` from `/app/core.c`. The compilation requires linking against the math library and compiling as position-independent code.
2. **Recover the calibration parameters**: Analyze the spoken audio file `/app/calibration.wav` to extract three integers. Let's call them A, B, and C (in the order they are spoken). You may use any transcription tool available (e.g., `whisper`, `ffmpeg`, or `espeak` if you need to reverse engineer).
3. **Build the Orchestrator & Server**: Write a Bash script `/app/run.sh` that:
   - Compiles the C library (runs `make`).
   - Starts a WebSocket server listening on `127.0.0.1:8765`. 
   - You can implement the WebSocket server using an inline Python script (via `websockets` and `ctypes` for FFI to the C library) launched by your Bash script.
4. **WebSocket Protocol**:
   - The server must accept incoming text messages in JSON format: `{"token": "A_B_C", "x": 10.5}` where `A`, `B`, and `C` are the digits from the audio file (e.g., `"token": "4_15_9"`).
   - If the token is incorrect or missing, the server should drop the connection or return an error.
   - If the token is correct, the server must load `libcore.so`, invoke `double process_value(double a, double b, double c, double x)` passing the extracted A, B, C parameters and the `x` value from the JSON.
   - The server must respond with JSON: `{"result": <calculated_value>}`.

Ensure your `/app/run.sh` script is executable, runs the server continuously, and correctly handles the FFI boundary between the dynamic language and the compiled C library. Leave the server running in the background when you are done.
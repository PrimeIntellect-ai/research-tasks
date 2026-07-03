I need you to build a polyglot service from scratch that decodes and evaluates a mathematical equation embedded in an audio signal. 

We are standardizing on Rust for our network edge, but our audio-processing routines are written in Go for rapid concurrent execution. You must set up the build system and write the code integrating these components.

Here are the specific requirements:

1. **Audio Artifact**: There is an audio file located at `/app/equation.wav`. It contains a sequence of DTMF (Dual-Tone Multi-Frequency) tones representing a simple mathematical expression (using digits 0-9, A for '+', B for '-', C for '*', D for '/').
2. **Go FFI Library (`libaudio.so`)**: 
   - Write a Go library that exposes a C-callable function: `char* EvaluateAudio(char* filepath)`.
   - The Go code must read the WAV file, decode the DTMF tones to extract the math string, evaluate the math expression, and return the numerical result as a C-string. 
   - You must use Go concurrency (goroutines) to process chunks of the audio file in parallel (e.g., splitting the file into segments and running the Goertzel algorithm concurrently).
   - Build this as a C-shared library (`libaudio.so`).
3. **Rust Edge Server**:
   - Create a Rust project that links against `libaudio.so` via FFI.
   - The Rust application must expose two network interfaces:
     a) An HTTP server listening on `127.0.0.1:8080`. It should have a route `GET /solve/dtmf`. It must require a Bearer token: `Authorization: Bearer polyglot-auth-token`. It should return a JSON response: `{"result": <evaluated_number>}`.
     b) A gRPC server listening on `127.0.0.1:50051`. Implement a protobuf service `MathSolver` with an RPC `SolveAudio(SolveRequest) returns (SolveResponse)`. The request contains the `filepath` (string), and response contains the `result` (int32).
4. **Build System**:
   - Provide a `build.sh` script in `/home/user/project` that compiles the Go library, configures the Rust C-bindings (using `build.rs` or standard linking), and compiles the Rust binary. 
   - Run the server in the background once built.

Please ensure the Rust server properly handles the FFI boundary, including memory management for the returned C-string from Go.
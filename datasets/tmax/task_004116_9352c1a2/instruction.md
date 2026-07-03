I need you to port a legacy C-based audio processing tool into a modern microservice architecture to run in a minimal container environment. 

You are provided with a legacy C project in `/home/user/audio_tool`. It contains the source code for an audio analysis tool that reads a WAV file and outputs a string representing the detected events. However, the project is currently broken. It fails to compile due to errors in the `Makefile` and a missing standard library inclusion in the C code. 

Your objectives are:

1. **Repair and Compile the C Tool**:
   - Fix the `Makefile` in `/home/user/audio_tool`. It currently fails to link properly (hint: it uses math functions but might be missing the appropriate linker flag) and may have formatting issues.
   - Fix any compilation errors in the C source files (e.g., missing headers).
   - Successfully compile the tool to produce the executable `/home/user/audio_tool/analyzer`.

2. **gRPC Service Design (Python)**:
   - Create a Protocol Buffers definition file at `/home/user/service/audio.proto`.
   - Define a service named `AudioAnalysis` with a single RPC method `Analyze`.
   - The `Analyze` method should accept a request containing a `string file_path` (the absolute path to a WAV file).
   - It should return a response containing a `string result_text`.

3. **Service Implementation**:
   - Write a Python gRPC server in `/home/user/service/server.py`.
   - Generate the necessary Python gRPC stubs from your `.proto` file.
   - Implement the `Analyze` method: when called, it should execute the compiled C program (`/home/user/audio_tool/analyzer <file_path>`), capture its standard output, and return that output in the `result_text` field. 
   - Strip any trailing newlines from the C program's output before sending the response.
   - The Python gRPC server must listen on `localhost:50051` without any TLS/authentication.
   - Keep the server running in the background or foreground so that it can accept requests.

An audio fixture is provided at `/app/test_audio.wav`. You do not need to process this file directly in your terminal, but ensure your gRPC server is up and running. An external verification script will connect to your service on port 50051, send a request with the path `/app/test_audio.wav`, and verify that the correct analysis result is returned.
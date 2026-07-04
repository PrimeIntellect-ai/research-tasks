You are a platform engineer maintaining our CI/CD pipelines. We have a pipeline that tests our embedded display system by recording its output to a video file. To automate the verification of these UI tests, we need a gRPC service that analyzes the video artifacts, interprets the visual output as bytecode instructions, and emulates the system's execution state.

Your task is to implement this gRPC service in Python.

**Requirements:**

1. **Protocol Definition:**
   Create a protobuf file named `ci_analyzer.proto` with the following specification:
   - Package: `ci_video`
   - Service: `CIAnalyzer`
   - RPC: `RunEmulator(RunRequest) returns (RunResponse)`
   - `RunRequest` has one string field: `video_path` (field number 1)
   - `RunResponse` has one repeated int32 field: `output` (field number 1)

2. **Video Analysis & Interpreter:**
   The video artifact (located at `/app/ci_test_run.mp4`) contains a sequence of solid colors flashing on screen, exactly 1 frame per second. You must extract the center pixel color at the 0.5s, 1.5s, 2.5s, etc. marks until the video ends or a HALT instruction is encountered.
   Map the colors to our custom stack-based VM instructions (use a threshold of >200 for high channels and <50 for low channels, standard RGB):
   - **Red** (High R, Low G, Low B): `PUSH 1`
   - **Green** (Low R, High G, Low B): `PUSH 2`
   - **Blue** (Low R, Low G, High B): `ADD` (pop two items, add them, push result)
   - **Yellow** (High R, High G, Low B): `MUL` (pop two items, multiply them, push result)
   - **Cyan** (Low R, High G, High B): `POP_OUT` (pop one item and append it to the response's output list)
   - **Black** (Low R, Low G, Low B): `HALT` (stop execution immediately)

3. **gRPC Server:**
   - Write a Python server (`server.py`) that implements the `CIAnalyzer` service.
   - The server must listen on `0.0.0.0:50051`.
   - The server must enforce authentication. It should check the gRPC metadata for an `authorization` key with the value `Bearer secret-token-123`. If missing or incorrect, abort with an UNAUTHENTICATED status.
   - When a valid request is received, it should analyze the video path provided, run the VM, and return the `RunResponse` containing the output list.

4. **Execution:**
   - You may use `ffmpeg` (via `subprocess`) or `opencv-python` to read the video.
   - Start the server as a background process or leave it running as the final step. Write a local log file to `/home/user/server.log` confirming startup.

Compile the protobufs, implement the server, and start it.
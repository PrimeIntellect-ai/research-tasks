You are an engineer porting a legacy video analysis tool to run as a microservice in a minimal container. Your task is to implement the core engine as a Python gRPC service, implement the numerical analysis algorithm, and create a setup script that mimics a CI/CD build step to compile the IDL and deploy the service locally.

There is a test video located at `/app/sample.mp4`. 

Step 1: gRPC Protobuf Definition
Create a file `/home/user/app/video.proto` with the following precise specification:
- `syntax = "proto3";`
- `package video;`
- A service named `VideoProcessor`.
- An RPC method named `AnalyzeFrameRange` that takes a `FrameRangeRequest` and returns a `FrameRangeResponse`.
- `FrameRangeRequest` must contain:
  - `int32 start_frame = 1;`
  - `int32 end_frame = 2;`
- `FrameRangeResponse` must contain:
  - `double average_variance = 1;`

Step 2: Service Implementation
Create a Python script at `/home/user/app/server.py` that implements this gRPC service and listens on `0.0.0.0:50051` (without any authentication).
The `AnalyzeFrameRange` method should perform the following numerical algorithm:
1. Extract the frames from `/app/sample.mp4` for the requested range `[start_frame, end_frame]` (both inclusive, 0-indexed).
2. Convert each extracted frame to grayscale using OpenCV's `COLOR_BGR2GRAY` conversion (which corresponds to `Y = 0.299 R + 0.587 G + 0.114 B`).
3. Calculate the population variance of the pixel intensities for each frame.
4. Calculate and return the arithmetic mean of these variances across the requested frame range.

Step 3: Build & Deployment Script
Write a bash script `/home/user/app/ci_setup.sh` that:
1. Installs any necessary Python dependencies (e.g., `grpcio`, `grpcio-tools`, `opencv-python-headless`, `numpy`).
2. Compiles the `video.proto` file into Python gRPC stubs.
3. Starts the `server.py` service in the background.
4. Saves the PID of the background server process to `/home/user/app/server.pid`.

Make sure `/home/user/app/ci_setup.sh` is executable. You must execute this script so the server is up and running, ready to be tested by the automated verifier.
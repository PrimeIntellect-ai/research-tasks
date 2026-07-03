You are an engineer tasked with setting up a polyglot build system and a gRPC service for a video analysis pipeline. 

We have a video file located at `/app/drone_flight.mp4`. Your objective is to expose a gRPC service in Python that extracts a specific frame from this video, computes a custom checksum on the raw frame data using a C library, and returns the result.

Here is the exact multi-stage workflow you must follow:

### 1. Polyglot Source Code Setup
Create a directory `/home/user/video_pipeline`. Inside, create a C file named `checksum.c` with the following implementation:
```c
#include <stdint.h>
#include <stddef.h>

// Computes a simple XOR-based checksum for error-checking
uint32_t compute_frame_checksum(const uint8_t* data, size_t length) {
    uint32_t checksum = 0x811c9dc5;
    for (size_t i = 0; i < length; i++) {
        checksum ^= data[i];
        checksum *= 0x01000193;
    }
    return checksum;
}
```

### 2. Build Orchestration
Create a shell script `/home/user/video_pipeline/build.sh` that acts as your CI/CD build step. This script must:
1. Compile `checksum.c` into a shared library named `libchecksum.so` using `gcc`.
2. Compile a Protobuf file into Python bindings using `grpc_tools.protoc`.

### 3. Protobuf Definition
Create `/home/user/video_pipeline/service.proto` with the following exact schema:
```protobuf
syntax = "proto3";
package video;

service FrameAnalyzer {
    rpc GetFrameChecksum (FrameRequest) returns (FrameChecksumReply) {}
}

message FrameRequest {
    int32 frame_number = 1;
}

message FrameChecksumReply {
    uint32 checksum = 1;
}
```

### 4. Service Implementation
Create a Python file `/home/user/video_pipeline/server.py`. This script must:
1. Start a gRPC server listening on `0.0.0.0:50051`.
2. Implement the `FrameAnalyzer` service.
3. When `GetFrameChecksum` is called with `frame_number = N`:
   - Open `/app/drone_flight.mp4` (e.g., using `cv2.VideoCapture`).
   - Read the exact 0-indexed frame `N`.
   - Convert the frame to Grayscale (`cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)`).
   - Flatten the grayscale frame into a contiguous 1D array of bytes.
   - Use Python's `ctypes` to load `libchecksum.so` and call `compute_frame_checksum(data, length)` on the flattened byte array.
   - Return the resulting checksum in the gRPC reply.

### 5. Execution
Make sure `build.sh` has executable permissions, run it to generate the artifacts, and then start `server.py` in the background so it is actively listening on port `50051`. Write a file `/home/user/video_pipeline/server.pid` containing the PID of your running Python gRPC server.
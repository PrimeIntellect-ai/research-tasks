You are a mobile build engineer investigating a critical failure in an offline CI runner. The runner failed to push its telemetry logs over the network, but we managed to capture a video of its diagnostic output matrix before the machine was wiped.

Your task is split into two phases: extracting the telemetry from the video, and building a C++ tool to process this telemetry format.

### Phase 1: Video Extraction
The diagnostic video is located at `/app/build_status.mp4`.
- The video runs at exactly 10 frames per second.
- The top-left pixel (x=0, y=0) acts as a serial data line. A white pixel `(255, 255, 255)` represents a binary `1`, and a black pixel `(0, 0, 0)` represents a binary `0`.
- Extract the bits sequentially, frame by frame, starting from frame 0.
- Pack the bits into bytes (8 bits per byte, Most Significant Bit first). E.g., the first 8 frames form the first byte.
- Save the resulting binary data to `/home/user/recovered_telemetry.bin`.

### Phase 2: Telemetry Processing Tool
The recovered binary data is a sequence of length-prefixed Protocol Buffer messages.
Each record consists of:
1. A 4-byte little-endian unsigned integer indicating the length of the protobuf message.
2. The serialized Protobuf message itself.

Create a Protobuf schema file named `telemetry.proto` in `/home/user/` with the following definition:
```protobuf
syntax = "proto3";
message Telemetry {
  uint64 timestamp = 1;
  string module_name = 2;
  bytes data = 3;
  uint32 crc32 = 4;
}
```

Write a C++ program, compiled to `/home/user/telemetry_sorter`.
The program must:
1. Read the length-prefixed stream from `stdin` until EOF.
2. Deserialize each message.
3. Validate the `crc32` field. It must exactly match the standard IEEE 802.3 CRC32 checksum of the `data` field. Discard the message if the checksum is invalid.
4. Sort the valid messages primarily by `timestamp` in ascending order, and secondarily by `module_name` in lexicographical ascending order (if timestamps are equal).
5. Print the sorted messages to `stdout`, one per line, strictly in this format:
   `[<timestamp>] <module_name>: <data_as_hex_string>`
   (Note: Use lowercase for the hex string, and print two characters per byte of `data`).

You may use system libraries. You will need to install `libprotobuf-dev`, `protobuf-compiler`, and `zlib1g-dev` (for CRC32) using `apt-get`. Write a `Makefile` or use raw g++ commands to compile your program.

Ensure your program `/home/user/telemetry_sorter` reads from standard input and prints to standard output, as it will be rigorously tested against thousands of simulated binary streams to verify its correctness.
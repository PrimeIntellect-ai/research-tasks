You are a mobile build engineer maintaining our secure CI/CD pipelines. We have a new security gate for our build assets: critical build configuration parameters are now distributed as audio memos (WAV) to prevent automated scraping of plaintext secrets from our internal repos, and they are verified via a microservice.

Your task is to implement this verification microservice in C++ using gRPC, integrate it with our C-based Error Correcting Code (ECC) library via FFI, and write a property-based test for the FFI wrapper.

Here are the requirements:

1. **Protobuf & gRPC Service (`/home/user/workspace/build_gate.proto`)**:
   Create a gRPC service named `AudioBuildGate` with an RPC `VerifyAsset`.
   - Request message `AssetRequest`: contains a single string field `file_path`.
   - Response message `AssetResponse`: contains a string `transcript`, a uint32 `checksum`, and a bool `is_valid`.

2. **C library FFI (`/home/user/workspace/ecc_lib.h` and `/home/user/workspace/libecc.so`)**:
   We have provided a compiled C library `libecc.so` at `/app/lib/libecc.so` (and its header at `/app/include/ecc_lib.h`). 
   It exposes a function: `uint32_t calculate_asset_crc(const uint8_t* data, size_t length);`
   Write a C++ wrapper class `EccValidator` that dynamically loads this library (or links against it via FFI/C bindings) and computes the CRC of a given file.

3. **Property-Based Testing (`/home/user/workspace/test_ecc.cpp`)**:
   Write a RapidCheck property test for your `EccValidator` wrapper. The property should assert that for any vector of bytes, appending a 0 byte changes the checksum (unless the initial data was empty, which you can skip). The test binary should be compiled to `/home/user/workspace/test_ecc_bin`.

4. **gRPC Server Implementation (`/home/user/workspace/server.cpp`)**:
   Implement the `AudioBuildGate` service in C++.
   When `VerifyAsset` is called:
   - Read the file at `file_path`.
   - Calculate the CRC using your `EccValidator`.
   - Transcribe the audio file. We have installed `whisper.cpp`'s main binary at `/usr/local/bin/whisper` and a base model at `/app/models/ggml-base.bin`. You can use `system()` or `popen()` to shell out to whisper to get the transcript of the audio file.
   - Set `is_valid` to `true` if the CRC is greater than 0, otherwise `false`.
   - Return the extracted `transcript`, `checksum`, and `is_valid` flag.
   
   The gRPC server must listen on `127.0.0.1:50051`. 
   Compile your server to `/home/user/workspace/gate_server` and run it in the background.

A test audio fixture is located at `/app/assets/config_memo.wav`. Once your service is running, write a log file at `/home/user/workspace/server_status.log` containing the exact line "SERVER READY". Our automated verification pipeline will wait for this file, then send gRPC requests to your server to test it against `/app/assets/config_memo.wav`.
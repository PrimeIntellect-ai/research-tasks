You are an algorithmic web developer building a secure data ingestion feature. We recently had an issue where our CI pipeline failed because our Python data ingestion service couldn't correctly communicate with our legacy C-based validation engine due to build orchestration and import ordering issues. 

Your task is to build a robust, polyglot data processing pipeline that extracts a transmitted message from an audio file, applies error correction, and passes it through a gRPC interface.

Here are the requirements:

1. **Audio Transcription**: 
   You have been provided with an audio file at `/app/transmission.wav`. This file contains a spoken sequence of binary digits (e.g., "zero", "one", "one", "zero"...). Transcribe this audio file into a continuous binary string. You may install and use any Python speech recognition libraries or CLI tools (like `whisper` or `ffmpeg`) available in standard repositories.

2. **Error Correction (Hamming 7,4)**:
   The binary string represents an ASCII message, but it has been encoded using a Hamming(7,4) error-correcting code. Additionally, there may be up to one single-bit flip per 7-bit block due to transmission noise.
   Write a C-language shared library (`libhamming.so`) that exposes a function to take a 7-bit block (as an integer or byte array), corrects any single-bit error, and extracts the original 4 bits of data.
   *Provide a Makefile* to orchestrate the build of this C library.

3. **gRPC Service**:
   Design a protobuf definition (`processor.proto`) with an RPC endpoint `rpc ProcessPayload(PayloadRequest) returns (PayloadResponse);`.
   Implement a Python gRPC server that uses `ctypes` to load your `libhamming.so`. The server should receive a raw binary string (the transcript), split it into 7-bit blocks, use the C library to decode and correct them into 4-bit nibbles, pack the nibbles into bytes, and decode the bytes into an ASCII string.

4. **Integration**:
   Write a Python client script that reads the audio file, performs the transcription, sends the binary string to the gRPC server, and receives the decoded ASCII string.
   
5. **Output**:
   The final decoded ASCII string must be saved exactly to `/home/user/decoded_output.txt`. Ensure the file contains only the decoded string with no trailing newlines or extra text.

Make sure your build process is reproducible and your gRPC imports are correctly ordered to avoid the CI issues we saw previously.
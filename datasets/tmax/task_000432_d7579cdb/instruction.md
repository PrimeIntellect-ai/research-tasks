You are a build engineer managing a legacy artifact processing pipeline. A critical component of the pipeline has been corrupted, but we have recovered its schema definition from a visual telemetry feed, and we have a buggy prototype of the parser in C. 

Your objective is to reconstruct the parser pipeline, fix the memory safety issues, and wrap it in a Python tool.

**Step 1: Recover the Protobuf Schema from Telemetry Video**
You have been provided with a telemetry video at `/app/telemetry.mp4`. The video encodes an ASCII text file. Every single frame in this video is a solid grayscale color. The grayscale intensity value (0 to 255) of each frame corresponds exactly to the ASCII decimal value of a character. 
Extract the frames, map the grayscale values to ASCII characters, and save the resulting string as `artifact.proto` in `/home/user/`. This file is a valid Protobuf schema.

**Step 2: Fix the C Parser**
In `/app/src/parser.c`, there is a C implementation for parsing a binary artifact header. The parser is supposed to read a stream of bytes, extract an integer ID, a flags byte, and a dynamic-length payload string, returning a populated C struct.
However, `parser.c` contains undefined behavior (buffer overflows) and memory leaks.
1. Fix the memory leaks and memory safety issues in `/app/src/parser.c`. Do not change the struct definitions or the function signature of `parse_header`.
2. Compile your fixed C code into a shared library at `/home/user/libparser.so`.

**Step 3: Create the Python Integration CLI**
Create a Python executable script at `/home/user/process_artifact.py`. 
This script must:
1. Compile and import the `artifact.proto` schema.
2. Read arbitrary raw binary data from `stdin` until EOF.
3. Pass the binary data to the fixed `parse_header` function in `libparser.so` using `ctypes`.
4. If the C parser returns a success code (0), populate the Protobuf message defined in `artifact.proto` using the returned data.
5. Write the serialized Protobuf message to `stdout`.
6. If the C parser returns an error code (non-zero), write nothing to `stdout` and exit with code 1.

The system will verify your script against a hardened oracle using millions of randomized byte sequences. Your Python script's `stdout` output must be bit-exact equivalent to the oracle.
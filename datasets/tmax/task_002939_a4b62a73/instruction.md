You are an integration developer responsible for migrating a legacy API security analysis tool from C to Python. You need to complete a multi-stage workflow involving video analysis, C compilation, protobuf parsing, and Python implementation.

Here are your tasks:

1. **Video Log Analysis**: 
   A colleague recorded a terminal session of an API traffic monitor, saved at `/app/api_traffic.mp4`. We need to know how many distinct frames contain the exact string `"ERROR: gRPC handshake failed"`. Extract this frame count and save it as a plain integer in `/home/user/video_count.txt`. You may use `ffmpeg` and OCR or strings analysis.

2. **Fixing the Legacy C Oracle**:
   The original C implementation of our payload parser is located in `/home/user/legacy_parser/`. It reads a binary file containing a serialized gRPC/protobuf message, parses it, applies a custom transformation to the payload, and prints a hex digest.
   - The `Makefile` in that directory is broken (spaces instead of tabs). Fix it.
   - Compile the program to produce `/home/user/legacy_parser/payload_parser`.

3. **Protobuf Compilation & Python Porting**:
   The protobuf schema for the API request is located at `/home/user/api_schema.proto`.
   - Compile this schema for Python.
   - Write a Python script at `/home/user/python_parser.py` that takes a single file path as a command-line argument.
   - The script must read the binary file, parse it using the generated protobuf class (`ApiRequest`), extract the `raw_payload` bytes field, reverse the byte order, and compute its MD5 hash.
   - The script must output ONLY the lowercase MD5 hex string to `stdout`, exactly matching the behavior of the C tool.

Your Python script (`/home/user/python_parser.py`) will be rigorously tested against a reference oracle with hundreds of randomly generated protobuf payloads to ensure absolute bit-exact equivalence. Ensure it handles edge cases (like empty payloads) identically to the C program.
You are a script developer tasked with building a web security analysis utility. A recent intrusion was captured not in standard logs, but via an experimental screen recording system that encoded intercepted web traffic data directly into the video feed as colored pixel blocks.

We need to extract this data, reconstruct the fragmented web requests using a highly optimized C library, and serve the results via a Python REST API. 

Here are the specific requirements:

**1. Video Extraction & Analysis**
We have a video artifact located at `/app/web_traffic_capture.mp4`. 
- Use `ffmpeg` to extract the frames.
- Every frame contains a single 8-bit value encoded in the RGB color of the pixel at coordinates (X=10, Y=10). The grayscale value (R=G=B) represents a single byte of data.
- Extract these bytes sequentially across all frames to create a raw binary payload file at `/home/user/extracted_payload.bin`.

**2. Core C Implementation (The Decoder)**
The binary payload contains fragmented HTTP requests. You must write a C program, `decoder.c`, that parses this binary stream.
- The stream consists of 8-byte chunks: `[2-byte chunk ID][2-byte total chunks][4-byte data payload]`.
- Implement a custom data structure (e.g., a balanced tree or a specialized hash map) to efficiently reassemble these chunks based on their `chunk ID`.
- Your C code must compile into two artifacts:
  a) A standalone executable `/home/user/decoder_cli` that takes the path to a binary file as an argument and prints the fully assembled data payloads to `stdout` in hexadecimal format, one assembled request per line, ordered by the lowest `chunk ID` first.
  b) A shared library `/home/user/libdecoder.so`.

**3. FFI & REST API**
Create a Python REST API using `Flask` or `FastAPI` in `/home/user/api.py`.
- Use Python's `ctypes` (FFI) to load `/home/user/libdecoder.so`.
- Expose a `GET /requests` endpoint that calls your C library to decode `/home/user/extracted_payload.bin` and returns the assembled hex strings as a JSON array.
- The server must run on port `8080`.

**4. Polyglot Build Orchestration**
Create a `Makefile` in `/home/user/` that:
- Compiles `decoder_cli` and `libdecoder.so`.
- Contains a `start-api` target that runs the Python API.

Your `decoder_cli` must exactly match the behavior of our reference implementation for any given valid or malformed binary payload, as it will be rigorously tested against random byte streams.
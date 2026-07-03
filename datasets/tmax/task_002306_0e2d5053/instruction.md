You are a storage administrator tasked with archiving and indexing legacy subtitle metadata to save disk space. A large batch of custom binary subtitle chunks needs to be processed, but first, you must create a reliable decoding tool. 

We have an original reference video file located at `/app/video/archive_footage.mp4`.
The legacy subtitle chunks are binary files that encode subtitle text for specific frames in the video.

You need to write a Python script at `/home/user/chunk_decoder.py` that reads exactly one binary subtitle chunk from **stdin** and prints the decoded output to **stdout**. 

The binary format of a valid subtitle chunk is exactly as follows:
1. **Magic Number** (4 bytes): Must be exactly `SUBZ` (ASCII). If not, output `INVALID_MAGIC` and exit.
2. **Encoding ID** (1 byte): An unsigned integer specifying the payload text encoding.
   - `0x01` = UTF-8
   - `0x02` = Shift-JIS
   - `0x03` = cp1252
   - If the ID is anything else, output `INVALID_ENCODING` and exit.
3. **Frame Number** (4 bytes): An unsigned big-endian integer.
4. **Payload Length** (2 bytes): An unsigned big-endian integer.
5. **Payload** (variable length): The encoded text bytes. 
   - If the stream ends before `Payload Length` bytes can be read, output `TRUNCATED_PAYLOAD` and exit.

**Validation and Decoding Rules:**
- The script must decode the payload using the specified encoding. Any invalid bytes during decoding should be replaced with `?` (the standard replacement character).
- The script must check the `Frame Number` against the actual video file (`/app/video/archive_footage.mp4`). 
- If the `Frame Number` is strictly greater than the **total number of frames** in the video, output `OUT_OF_BOUNDS` and exit.
- Otherwise, on success, print the following exact format to stdout:
  `FRAME_{frame_number_zero_padded_to_6_digits}: {decoded_payload_text}`

Your script must be executable (`chmod +x`) and begin with `#!/usr/bin/env python3`. It must handle raw bytes from stdin (e.g., `sys.stdin.buffer.read()`).
To complete the task, analyze the video to determine the total frame count, write the script, and ensure it exactly meets the specification.
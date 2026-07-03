You are an AI assistant helping a researcher organize and sanitize dataset archives. We receive sensor data logs mixed with video frames, but some of the binary data logs have become corrupted during transmission.

Your task has two parts:

Part 1: Video Fixture Processing
We have a reference recording at `/app/experiment.mp4`. 
1. Extract the video frame at exactly 00:00:02.500 (2.5 seconds).
2. Convert this single frame to a raw 8-bit grayscale binary format (`.raw` / gray format in ffmpeg) with a resolution of 640x480.
3. Save the resulting raw binary data to `/home/user/reference_frame.raw`.

Part 2: Dataset Sanitization Tool
We have thousands of binary `.dat` files, some of which are structurally corrupted ("evil") and some are perfectly intact ("clean").
Write a C++ program in `/home/user/sanitizer.cpp` and compile it to `/home/user/sanitizer`.

The `sanitizer` executable must take exactly one argument: the path to a `.dat` file.
Invocation: `./sanitizer <path_to_dat_file>`

It must parse the `.dat` file and determine if it is clean or corrupted.
A clean `.dat` file MUST strictly adhere to the following binary format:
- Offset 0: Magic string `SENSORDT` (8 bytes, exactly these ASCII characters, no null terminator needed if it fills the 8 bytes)
- Offset 8: Frame Index (4 bytes, unsigned 32-bit integer, little-endian)
- Offset 12: Payload Size (4 bytes, unsigned 32-bit integer, little-endian)
- Offset 16: Payload Data (Exactly `Payload Size` bytes)

A file is considered "evil" (corrupted) if ANY of the following are true:
- It is smaller than 16 bytes.
- The 8-byte magic string does not exactly match `SENSORDT`.
- The actual remaining file size after the 16-byte header does NOT exactly match the `Payload Size` specified in the header. (e.g. truncated or padded with extra junk).

Behavior:
- If the file is strictly valid ("clean"), the program must exit with status code `0`.
- If the file is invalid/corrupted ("evil"), the program must exit with status code `1`.

Make sure to compile your C++ program so the executable is available at `/home/user/sanitizer`. You may use standard C++ libraries. No external libraries are required.
You are a performance engineer tasked with modernizing a legacy video profiling system. 

We have a legacy compiled binary located at `/app/legacy_analyzer`. This tool accepts a raw 8-bit grayscale image file (1 byte per pixel) as its first argument and prints a calculated integer "profiling score" to standard output. 

Unfortunately, this binary is prone to crashing due to a numerical instability when processing certain edge-case frames in our test datasets. 

Your task is to:
1. Extract frames from a test video located at `/app/test_sequence.mp4`.
2. Reverse engineer the `legacy_analyzer` binary to understand the exact mathematical formula it uses to calculate the "profiling score" from the raw grayscale pixel bytes.
3. Identify the boundary condition / numerical instability that causes the binary to crash on specific frames.
4. Write a new, robust HTTP service in the language of your choice that replicates this scoring logic but fixes the crash. 

Your HTTP service must meet the following specifications:
- Listen on `127.0.0.1:9000`.
- Expose a single endpoint: `GET /score?frame=<N>` where `<N>` is the 0-indexed frame number.
- When a request is received, your service should extract the N-th frame from `/app/test_sequence.mp4` (as an 8-bit grayscale image) and calculate the score using the reversed algorithm.
- If the frame contains pixel data that would have triggered the numerical crash (e.g., a divide-by-zero or overflow in the original algorithm), your service must catch this boundary condition and return `-1` in the HTTP response body.
- Otherwise, return the calculated integer score as plain text.

The service should remain running in the foreground or background so that an automated test suite can issue multiple `GET` requests to verify its accuracy and stability. `ffmpeg` is installed on the system for your frame extraction needs.
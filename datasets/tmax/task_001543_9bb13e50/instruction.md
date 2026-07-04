You are a performance engineer tasked with debugging and profiling a critical data extraction pipeline.

We have a multithreaded C program located at `/home/user/frame_decoder.c`. This program is designed to take raw 8-bit grayscale frame data (exactly 4096 bytes representing a 64x64 frame), decode a payload from it using 4 worker threads, and print the resulting integer payload to `stdout`.

Unfortunately, the program currently suffers from a race condition and memory corruption issue. When it encounters "corrupted" frames (specifically, frames where the first 4 bytes do not match a known magic header), the threads improperly access a shared error-tracking state, leading to intermittent segmentation faults (core dumps).

Additionally, as part of your performance profiling, you need to run this decoder on a real video feed. The video artefact is located at `/app/profiling_target.mp4`. 

Your tasks are:
1. **Debug and Fix:** Use tools like `gdb`, core dump analysis, or `strace` to identify the race condition and corrupted input handling bug in `/home/user/frame_decoder.c`. Fix the C code so that it is thread-safe and gracefully exits with a return code of `1` (printing nothing) when it encounters a corrupted frame, without crashing.
2. **Compile:** Compile your fixed program to `/home/user/frame_decoder`.
3. **Equivalence:** Your fixed `/home/user/frame_decoder` must behave exactly like our slow, single-threaded reference implementation (an oracle). The automated verifier will aggressively test your binary against the oracle using thousands of random 4096-byte inputs to ensure it is bit-exact in both standard and corrupted input scenarios.
4. **Pipeline Execution:** Use `ffmpeg` to extract the raw 8-bit grayscale frames (`gray` pixel format, 64x64 resolution) from `/app/profiling_target.mp4`. Pass each 4096-byte frame into your fixed `/home/user/frame_decoder`.
5. **Aggregation:** Sum the integer outputs from all the *valid* frames in the video. Write this final single integer sum to `/home/user/video_sum.txt`.

Constraints:
- You must write your fixes in C.
- Do not change the expected size of the input buffer (4096 bytes).
- Ensure your compiled binary is executable and placed exactly at `/home/user/frame_decoder`.
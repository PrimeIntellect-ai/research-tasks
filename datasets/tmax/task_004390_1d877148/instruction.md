You are a platform engineer maintaining CI/CD pipelines. We recently started recording our automated UI test runs as video files. To analyze these test runs faster, we need to replace our slow legacy analysis tool with a highly optimized C shared library and CLI utility.

We have a legacy compiled tool located at `/app/oracle_analyzer`. It takes a single command-line argument: the path to a raw RGB24 binary file representing a single 64x64 pixel video frame. It reads the 12,288 bytes (64 * 64 * 3) and outputs a single status string to stdout (either "PASS", "FAIL", "FLAKY", or "CORRUPT") followed by a newline.

Your task is to:
1. Deduce the exact logic used by `/app/oracle_analyzer`. You can do this by generating raw RGB24 binary files, passing them to the oracle, and observing the output.
2. Implement this exact logic in C. Create a shared library named `/home/user/libframeparser.so` that exports a function with the signature: `void decode_ci_status(const unsigned char* rgb_data, char* status_out);`
3. Create a CLI frontend in C named `/home/user/analyzer_cli` that links against `libframeparser.so`. It must take a filepath as its first argument, read exactly 12,288 bytes from the file into an array, call `decode_ci_status`, and print the resulting string to stdout with a trailing newline. The behavior must be perfectly bit-for-bit equivalent to `/app/oracle_analyzer` for any possible 12,288-byte input.
4. We have a sample CI run video located at `/app/ci_test_run.mp4`. Use `ffmpeg` to extract the frames of this video as raw 64x64 RGB24 binary files.
5. Process every extracted frame sequentially using your `/home/user/analyzer_cli` tool.
6. Compile the results into a final log file at `/home/user/ci_report.txt`. Each line of this file should contain the frame number (starting at 1) and the status, e.g., `Frame 1: PASS`.

Constraints:
- You must write your solution in C.
- You must manage the ABI and compilation manually using standard build tools (gcc, ld).
- The verifier will aggressively fuzz your `analyzer_cli` against `oracle_analyzer` with millions of random inputs to ensure absolute equivalence. Do not just handle the cases present in the video.
You are a mobile build engineer maintaining a video processing pipeline. We have a Go service that acts as a wrapper around a high-performance C library for generating Adler-32 checksums on raw video frames. However, the pipeline is currently broken due to a memory safety issue in the C code, and the Go service needs to be completed, benched, and cross-compiled for our mobile architectures.

Your objectives:

1. **Fix the C Code**: 
   The file `/home/user/src/checksum.c` contains a memory safety bug (an out-of-bounds read) that causes undefined behavior and crashes during checksum calculation. Identify and fix this bug.

2. **Complete the Go Service**:
   In `/home/user/src`, create a Go HTTP service (`main.go`) that:
   - Listens on `127.0.0.1:8080`.
   - Exposes a `POST /process` endpoint.
   - Accepts a JSON payload: `{"video_path": "<path>"}`.
   - Uses `os/exec` to run `ffmpeg` and extract exactly the first 10 frames of the provided video as raw RGB24 data. Command format:
     `ffmpeg -i <video_path> -vframes 10 -f image2pipe -vcodec rawvideo -pix_fmt rgb24 -`
   - Reads the standard output of the `ffmpeg` command into a single byte slice.
   - Uses `cgo` to pass this byte slice to the `calculate_checksum` function in `checksum.c`.
   - Returns a JSON response: `{"checksum": <uint32_result>}`.

3. **Benchmarking**:
   Write a benchmark in `/home/user/src/checksum_test.go` that benchmarks the Go wrapper calling the C function with a dummy byte slice of 1MB (1024 * 1024 bytes). Run the benchmark and save the output to `/home/user/bench.txt`.

4. **Cross-Compilation**:
   Cross-compile your Go service for both `linux/arm64` and `linux/amd64`. Place the compiled binaries in `/home/user/build/` and name them `server_arm64` and `server_amd64` respectively. CGO must be enabled for both cross-compilations (you may need to install appropriate C cross-compilers like `gcc-aarch64-linux-gnu`).

Start the HTTP server in the background on port 8080 before completing your turn. A test video is provided at `/app/test_video.mp4`.
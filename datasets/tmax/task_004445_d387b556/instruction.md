You are an engineer tasked with porting a legacy Web Security video scanning tool to a minimal container environment. The original tool was written in Go but currently fails to build due to a circular import introduced in the latest commit. Your goal is to rewrite the core processing logic in Python, interface with the underlying C security library, analyze a surveillance video, and set up a reverse proxy.

Here are your specific objectives:

1. **Shared Library Management**:
   In `/home/user/sec_lib/`, there is C source code (`scanner.c` and `scanner.h`) for a security library. Compile this into a shared library named `libsecscan.so`. The library exposes a function `calculate_threat` which takes a specific ABI structure. Look at the C header to understand the `frame_data` struct (which contains an integer ID and a 32-byte SHA256 hash).

2. **Python Implementation**:
   Write a Python script at `/home/user/py_scanner.py`. This script must act as a drop-in replacement for the Go tool. 
   - It should read exactly 36 bytes from standard input (stdin) at a time (representing the 4-byte little-endian integer ID, followed by the 32-byte raw hash).
   - Use `ctypes` to correctly map the ABI and pass this data to the `calculate_threat` function in `libsecscan.so`.
   - Print the returned threat score (a 32-bit float) to standard output (stdout) formatted to 4 decimal places (e.g., `Threat: 0.8421`), followed by a newline.
   - Loop and continue reading until EOF. 
   - Note: You can look at the broken Go source in `/home/user/go_legacy/` to understand how the concurrency and channels used to pass these structs, but your Python script just needs to handle the binary standard input synchronously or asynchronously.

3. **Video Artifact Analysis**:
   There is a video fixture located at `/app/surveillance.mp4`. 
   - Use `ffmpeg` to extract exactly frame 142 from this video.
   - Calculate the raw SHA256 hash (in binary form, not hex) of the extracted frame (saved as a JPEG).
   - Pass a mock frame ID of `142` and this 32-byte raw hash to your Python script.
   - Save the exact stdout output of your script for this specific frame to `/home/user/frame142_threat.txt`.

4. **Reverse Proxy Configuration**:
   The final container needs a reverse proxy. Write a minimal Nginx configuration at `/home/user/proxy.conf` that listens on port `8080`. All HTTP POST requests to the `/scan` endpoint should be reverse-proxied to a backend running on `127.0.0.1:9000`. (You do not need to build the backend HTTP server that wraps your python script, just configure the Nginx proxy routing).

Ensure your Python script `py_scanner.py` perfectly matches the binary input/output behavior described above, as it will be rigorously tested against an existing oracle binary.
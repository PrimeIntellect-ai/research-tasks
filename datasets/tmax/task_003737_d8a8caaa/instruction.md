You are acting as a Site Reliability Engineer investigating a recurring outage in our legacy metric aggregation service. 

We received a screenshot of a dashboard from the exact moment the service crashed last night, located at `/app/crash_alert.png`. The screenshot contains the base64-encoded payload that caused the service to segfault. Use an OCR tool (like `tesseract`) to extract the exact crashing payload from this image.

The source code for the service is located at `/home/user/metrics_server.c`. It is a simple C TCP server that reads a base64-encoded string, decodes it into a local buffer, and responds. Unfortunately, it crashes when it receives the corrupted/oversized input shown in the screenshot due to a buffer overflow.

Your task:
1. Extract the base64 payload from `/app/crash_alert.png`.
2. Debug and patch `/home/user/metrics_server.c` to prevent the buffer overflow. The server must be fixed such that:
   - If the decoded payload length is exactly 16 bytes or fewer, it should process it safely and return `OK\n`.
   - If the decoded payload exceeds 16 bytes, it must NOT crash. Instead, it must catch the size boundary and return `ERR: OVERFLOW\n`.
3. Compile your fixed version using `gcc /home/user/metrics_server.c -o /home/user/metrics_server`.
4. Run the fixed service in the background, listening on `127.0.0.1:9090`.

Leave the service running on port 9090 so our automated test suite can connect via TCP, send the crashing payload (along with random fuzzed inputs), and verify the service handles them gracefully without crashing.
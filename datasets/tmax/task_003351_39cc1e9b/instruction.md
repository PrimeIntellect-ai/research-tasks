You are tasked with building a streaming ETL script in Bash that processes video feature extraction requests, while maintaining internal state to prevent duplicate processing on retry events. 

A video artefact is provided at `/app/surveillance.mp4`. 
We have a simulated streaming source that sends extraction requests via standard input to your script. Since the upstream system has flaky retries, it often sends duplicate requests for the same timestamp. 

Create a Bash script at `/home/user/process_stream.sh`.
The script must:
1. Read lines from standard input, one by one.
2. Each line will have the format: `EVENT_ID TIMESTAMP` (e.g., `101 00:00:05`, `102 00:00:12`).
3. Maintain a state tracking which `TIMESTAMP`s have already been processed during the script's execution.
4. For each line:
   a. If the `TIMESTAMP` has already been seen in the current stream, output exactly: `DUPLICATE <TIMESTAMP>` (e.g., `DUPLICATE 00:00:05`) to standard output.
   b. If the `TIMESTAMP` is new, use `ffmpeg` to extract the single frame at that exact timestamp from `/app/surveillance.mp4`.
      - Output the frame to standard out (stdout) as JPEG (`-f image2 -c:v mjpeg`).
      - Scale the frame to `160x120` (`-s 160x120`).
      - Suppress all ffmpeg logging (`2>/dev/null`).
      - Pipe the jpeg bytes to `sha256sum` to compute its hash.
      - Output exactly: `NEW <TIMESTAMP> <SHA256>` to standard output.

Constraints:
- The script must be executable (`chmod +x`).
- Do not create any permanent files on disk for the extracted frames; data must be streamed directly from `ffmpeg` to `sha256sum`.
- Your script must perfectly match the output of our reference implementation for any given valid input stream.
- Handle standard input efficiently.

Example input:
```
1 00:00:01
2 00:00:03
3 00:00:01
```

Example output:
```
NEW 00:00:01 3b4a2...
NEW 00:00:03 8f1d7...
DUPLICATE 00:00:01
```

Write the script and ensure it handles stream processing correctly.
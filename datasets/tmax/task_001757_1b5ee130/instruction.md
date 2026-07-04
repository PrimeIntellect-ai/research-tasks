You are acting as a deployment engineer rolling out a lightweight video frame streaming update. You have been provided with a deployment feed video at `/app/deployment_feed.mp4`. Your task is to extract frames from this video and write a custom C-based TCP server to stream these frames upon request.

Here are the specific steps to complete the rollout:

1. **Frame Extraction**: 
   Write a bash script to extract frames from `/app/deployment_feed.mp4` at exactly 1 frame per second.
   Save these frames in `/home/user/frames/` with the naming convention `frame_%04d.jpg` (e.g., `frame_0001.jpg`, `frame_0002.jpg`). Use `ffmpeg` for this.

2. **Streamer Service (C)**:
   Write a C program, saved at `/home/user/streamer.c`, that implements a custom TCP frame-serving protocol.
   - The server must listen on TCP port `8888` on the `127.0.0.1` interface.
   - It should accept incoming connections. For each connection, it should read a single line ending in a newline (`\n`). This line will contain exactly a 4-digit frame number (e.g., `0005`).
   - The server must locate the corresponding frame file in `/home/user/frames/`.
   - If the frame file exists, the server must respond with `OK <size_in_bytes>\n`, followed immediately by the raw binary contents of the JPEG file.
   - If the frame file does not exist, or the input is malformed, the server must respond with `ERR\n`.
   - After sending the response, the server should close that client connection and continue listening for new connections.

3. **Deployment**:
   Compile the C program into an executable named `/home/user/streamer`. Start the server in the background so it is actively listening on `127.0.0.1:8888`. Ensure it stays running.

Your final setup will be tested by an automated verifier that will make real TCP requests to your server for various frames and validate both the protocol framing and the binary JPEG data returned.
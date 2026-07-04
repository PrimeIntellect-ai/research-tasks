You are a data engineer building a micro-ETL pipeline for video frame analysis. We are migrating our pipeline to Rust for performance.

We have a video feed located at `/app/video_feed.mp4`. 

Your task is to write and run a simple Rust HTTP service that handles frame extraction, caching (simulating large-scale storage management), and simple binary classification based on frame complexity.

Please create a Rust project in `/home/user/frame_etl` and write a server that listens on `127.0.0.1:9090`. 

The service must implement a single HTTP GET endpoint:
`GET /process?sec=<N>` (where `<N>` is an integer representing seconds).

When this endpoint is hit, your Rust service must:
1. Check if the frame for second `<N>` already exists in the local storage directory `/home/user/datastore/frame_<N>.jpg`.
2. If it does not exist, use `ffmpeg` (as a subprocess) to extract the frame at exactly that second from `/app/video_feed.mp4` and save it to `/home/user/datastore/frame_<N>.jpg`. Use `-q:v 2` for the jpeg quality.
3. Read the file size (in bytes) of the extracted `.jpg`.
4. Perform a simple classification: if the file size is strictly greater than 40,000 bytes, classify it as `"Complex"`, otherwise `"Simple"`.
5. Return a strict JSON response with a 200 OK status. Format:
   `{"second": <N>, "size": <bytes>, "classification": "<Complex|Simple>"}`

Requirements:
- You must create the `/home/user/datastore` directory.
- Use standard Rust libraries (`std::net::TcpListener`) or a lightweight framework like `axum` or `actix-web` (you can initialize with `cargo new` and add dependencies as needed).
- Leave the server running in the background (or foreground if you multiplex the terminal) so our test suite can issue HTTP requests to it.

Ensure the service is fully running and listening on `127.0.0.1:9090` before completing the task.
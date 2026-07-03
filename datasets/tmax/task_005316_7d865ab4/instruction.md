You are a platform engineer maintaining our CI/CD pipelines. We have a suite of end-to-end UI tests that frequently fail. To better debug these, we record the test sessions and emit structured logs. 

Your task is to create a Rust-based diagnostic service that correlates visual test failures with CI pipeline logs. 

Here are the requirements:

1. **Video Analysis**: 
   A screen recording of the latest failed UI test run is located at `/app/ci_test_recording.mp4`. The video is encoded at 1 frame per second. Whenever the UI encounters a catastrophic error, a bright solid red square (color `#FF0000`, at least 50x50 pixels) appears somewhere on the screen for exactly one frame. 
   You must use `ffmpeg` (which is preinstalled) from within your Rust application or via a shell script invoked by Rust to extract the frames and analyze them to find the exact timestamps (in seconds, starting from 0) where these red squares appear.

2. **WebSocket Server**:
   Write a Rust application that starts a WebSocket server listening precisely on `127.0.0.1:9001`. 
   - The server must require clients to pass an authorization header during the HTTP upgrade request: `Authorization: Bearer secret-ci-token`. Connections without this exact token must be rejected with a 401 status code.
   - Upon a successful WebSocket connection, the client will send a single text message containing a JSON array of log events. Each log event has the format: `{"timestamp_sec": 12, "event_msg": "Network timeout", "source": "backend"}`.

3. **Data Transformation and Output**:
   - Parse the incoming JSON.
   - Combine the log events with the visual errors detected in the video. A visual error should be modeled as an event: `{"timestamp_sec": <sec>, "event_msg": "Visual Error Detected", "source": "ui_test"}`.
   - Merge both data streams, sort them chronologically by `timestamp_sec` (ascending). If a log event and a visual error have the exact same timestamp, the visual error should appear *after* the log event in the sorted array.
   - Format the combined, sorted array as a strictly formatted JSON array.
   - Send this JSON string back over the WebSocket connection to the client as a single text message.
   - Close the WebSocket connection gracefully.

You must build and run this service so it is actively listening on port 9001. Ensure your Rust project is initialized in `/home/user/ci_analyzer` and that you leave the service running in the background when you consider the task complete. You may use any standard Rust crates (e.g., `tokio`, `tungstenite`, `serde_json`, `image`).
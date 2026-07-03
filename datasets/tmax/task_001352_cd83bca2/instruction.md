You are a QA engineer setting up a polyglot test environment for our video analysis web pipeline. We have a partially implemented system that processes video files, but it needs debugging, schema migration, and a multi-protocol service wrapper.

Here are your objectives:

1. **Rust Debugging & Polyglot Build:**
   There is a Rust CLI project located at `/app/rust_counter`. It is supposed to accept a string, count the number of words, and print it. However, the original developer left a borrow checker error in `src/main.rs`. 
   - Fix the Rust code so it compiles.
   - Build the release binary.

2. **Schema Migration:**
   We have a SQLite database at `/app/video_stats.db` with an existing table: `CREATE TABLE stats (video_name TEXT, frames INTEGER)`. 
   - Write a Python script to migrate this schema by adding a new column `anomalies INTEGER DEFAULT 0`.
   - Update the existing row for `traffic.mp4` to have `anomalies = 3`.

3. **Video Processing & Expression Evaluation:**
   We have a test video fixture at `/app/traffic.mp4`.
   - Use `ffmpeg` (which is preinstalled) to extract exactly frame 30 from `/app/traffic.mp4` and save it to `/app/frame_30.jpg`.

4. **Multi-Protocol Web Service (Python):**
   Create a Python service that runs continuously and listens on two ports.
   - **HTTP (Port 8000):** 
     Provide a `POST /evaluate` endpoint that accepts JSON like `{"expr": "3 + 5 * 2"}`. You must implement a simple expression parser in Python (supporting only integers, `+`, `-`, `*`, `/`, and standard operator precedence) and return JSON `{"result": 13}`. Do not use `eval()`.
     Provide a `GET /frame` endpoint that returns the `/app/frame_30.jpg` file.
   - **Raw TCP (Port 8001):**
     Listen for incoming raw TCP connections. When a string expression (like "10 - 2\n") is received, parse and evaluate it using the same logic as above, send back the integer result as a string followed by a newline (e.g., "8\n"), and close the connection.

Ensure your Python service is running in the background and listening on both `0.0.0.0:8000` and `0.0.0.0:8001` before you finish.
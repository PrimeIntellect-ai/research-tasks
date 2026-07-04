You are an automation specialist tasked with building a video scene-analysis workflow. We need to analyze a video, detect changes between consecutive seconds, and serve the results via an API.

Your objective is to orchestrate a pipeline that extracts frames from a video, calculates the visual difference between them, saves the data to disk, and serves it over HTTP. You must use Rust to implement the analysis and the web server.

Here are the specific requirements:

1. **Frame Extraction**:
   There is a video file located at `/app/source_video.mp4`.
   Use `ffmpeg` to extract exactly 1 frame per second from this video. Save the frames as PNG images in `/home/user/frames/` using the naming convention `frame_0001.png`, `frame_0002.png`, etc.

2. **Distance Computation (Rust)**:
   Create a Rust project in `/home/user/video_analyzer`. Write a program that reads the extracted PNG frames in sequential order.
   For each consecutive pair of frames (e.g., frame 1 and 2, frame 2 and 3), compute the Grayscale Mean Absolute Difference (MAD).
   * MAD Definition: Convert both images to 8-bit Grayscale. For every pixel `(x,y)`, calculate the absolute difference in the 8-bit pixel values: `|P1(x,y) - P2(x,y)|`. The MAD is the sum of these absolute differences divided by the total number of pixels in the image.

3. **Multi-format Output**:
   The Rust program must output the calculated distances into a CSV file at `/home/user/distances.csv`.
   The CSV must have the exact headers: `start_frame,end_frame,mad` (where `start_frame` and `end_frame` are integers, e.g., 1 and 2, and `mad` is formatted to 2 decimal places).

4. **HTTP API Server**:
   The same Rust program must subsequently start an HTTP server listening on `127.0.0.1:8000`.
   The server must implement two routes:
   * `GET /api/distances`: Returns a JSON array of the computed differences. Example: `[{"start_frame": 1, "end_frame": 2, "mad": 15.22}, {"start_frame": 2, "end_frame": 3, "mad": 3.05}]`
   * `GET /api/frames/<id>`: Returns the raw PNG file for the requested frame (e.g., `/api/frames/1` should serve `frame_0001.png` with the correct `image/png` content type).

Ensure your Rust server remains running in the background or foreground so that it can be tested. You may use any standard Rust crates (e.g., `image`, `axum`, `tokio`, `serde`, `csv`).
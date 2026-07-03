We are replacing a legacy Rust-based video integrity microservice that fails to compile in our minimal Linux container environment due to library issues. Your task is to implement a lightweight Python 3 replacement that performs video frame extraction, checksumming, and numerical analysis.

You must write a zero-dependency Python script (using standard libraries like `http.server`, `zlib`, `subprocess`, and `time`) that provides an HTTP REST API. It must rely only on the pre-installed `ffmpeg` CLI tool to read video data.

**Requirements:**
1. **Listen Address**: The server must listen on `127.0.0.1:9090`.
2. **Data Source**: The target video file is located at `/app/test_feed.mp4`.
3. **Endpoints**:
   
   - `GET /analyze?frame=<N>`
     Extract the `<N>`-th frame of `/app/test_feed.mp4` (1-indexed). You must extract ONLY the grayscale (luminance) channel. Use `ffmpeg` to extract the raw grayscale frame bytes (e.g., using `-pix_fmt gray` and `-f image2pipe`). 
     Compute two values:
     * `crc32`: The CRC32 checksum of the raw frame bytes (using `zlib.crc32`).
     * `luma_sum`: A numerical algorithm result calculating the sum of all pixel intensity values in the frame.
     * **Response Format**: A JSON object: `{"frame": <N>, "crc32": <integer>, "luma_sum": <integer>}`.
     * Ensure HTTP 200 OK is returned with the correct `Content-Type: application/json`.

   - `GET /benchmark`
     Perform a performance benchmark by running the analysis (extracting raw bytes, computing CRC32, and calculating `luma_sum`) sequentially on frames 1, 2, 3, 4, and 5.
     Measure the wall-clock time it takes to perform this loop (including `ffmpeg` invocations).
     * **Response Format**: A JSON object: `{"frames_processed": 5, "time_ms": <float_milliseconds>}`.

Start the server in the background so it is ready to receive requests. Do not use external Python packages like Flask, FastAPI, or OpenCV; stick to the Python standard library and `ffmpeg`.
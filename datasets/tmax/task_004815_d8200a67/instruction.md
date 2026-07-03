You are a performance engineer tasked with debugging a scientific analysis web service. 

We have a video artefact of an experiment located at `/app/sensor_data.mp4`.
We also have a C-based HTTP server, `/app/analyzer.c`, which is supposed to analyze specific frames of this video. The server listens on port `9090` and exposes an endpoint `/analyze?frame=N`. 

When requested, the server:
1. Reads the `N`th frame from the video (you may pre-extract the frames to `/app/frames/` as 8-bit grayscale raw files, size 640x360).
2. Converts the frame to a 2D `double` matrix.
3. Computes the column sums of the matrix.
4. Uses a multi-threaded approach to compute a global weighted sum of these column sums.

**The Problem:**
Due to floating-point reduction order in the multi-threaded sum in `/app/analyzer.c`, the API returns slightly different results on subsequent calls for the same frame. It is currently using a naive shared accumulator with a mutex, causing non-deterministic addition order.

**Your objectives:**
1. **Environment Setup:** Install necessary libraries (e.g., `ffmpeg`, `libmicrohttpd-dev`, `build-essential`).
2. **Video Processing:** Extract the first 50 frames of `/app/sensor_data.mp4` to `/app/frames/frame_N.gray` (where N is 1-indexed, no zero-padding). The frames should be 640x360, 8-bit grayscale.
3. **Fix the C Server:** Modify `/app/analyzer.c` to use a deterministic summation method (e.g., allocate an array for per-thread partial sums, then sum them sequentially in thread-index order at the end). Compile it to `/app/analyzer` and leave it running in the background listening on `0.0.0.0:9090`.
4. **Data Visualization:** Write a Python script `/app/visualize.py` that queries the running server for frames 1 to 50, saves the frame numbers and deterministic sums to `/app/results.csv` (headers: `frame,sum`), and generates a line plot in `/app/plot.png`.

The HTTP response from the C server must be just the floating-point sum as a string, formatted with `%f`.

Ensure the server is running when you finish, as an automated verifier will make requests to `http://localhost:9090/analyze?frame=X` to ensure the non-determinism is fixed and the math is correct.
You are a platform engineer maintaining a CI/CD pipeline. One of our tasks is to retroactively analyze video recordings of E2E test runs (e.g., terminal outputs and browser screens) to pinpoint exactly when a build fails. We do this by detecting "red screens" (error outputs).

We are migrating our slow Python-based video analyzer to a polyglot architecture: a fast C core for pixel processing, orchestrated by a Node.js REST API.

Your tasks:

1. **Fix the API Environment:**
   In `/home/user/api`, there is a Node.js project for our REST API. The `npm install` command currently fails due to conflicting peer dependencies between our logging library and the web framework. Resolve these conflicts so you can successfully install the dependencies and run the server.

2. **Implement the C Frame Analyzer:**
   Create a C program at `/home/user/analyzer/frame_analyzer.c` and a `Makefile` to compile it to `/home/user/analyzer/frame_analyzer`.
   This program must process raw RGB24 pixel data from `stdin` (a stream of bytes, reading until EOF) and compute a "Red Dominance Score" using this exact numerical algorithm:
   - Initialize a 64-bit integer `total_score` to 0.
   - Read the input stream in 3-byte chunks (representing R, G, B). Ignore any trailing bytes that don't form a complete 3-byte pixel.
   - For each pixel: if `R > (G + B)`, add `(R - G - B)` to `total_score`.
   - After processing all bytes, output a single line to `stdout` containing the result of `total_score % 1000003`.

3. **Complete the API endpoint:**
   Update the Node.js API in `/home/user/api/index.js` (or similar, create if missing) to expose a `GET /analyze?frame=N` endpoint.
   When called, the endpoint must:
   - Use `ffmpeg` to extract exactly frame `N` from the video artifact `/app/terminal_e2e.mp4`. Output the frame as raw video (`-f rawvideo`), pixel format `rgb24`, and pipe it directly to your compiled C binary (`/home/user/analyzer/frame_analyzer`).
   - Return a JSON response: `{ "frame": N, "score": <computed_score> }`.

4. **Integration & Execution:**
   Start the API on port 3000. Write a script to iterate over frames 0 to 100 (inclusive) of `/app/terminal_e2e.mp4` via the API.
   Determine which frame has the highest "Red Dominance Score".
   Output the result as JSON to `/home/user/highest_frame.json` in the exact format: `{"frame": <N>, "score": <S>}`.
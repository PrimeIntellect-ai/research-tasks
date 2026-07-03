You are a bioinformatics analyst tasked with processing a time-lapse fluorescence video from a novel microarray flow cell. The raw video is located at `/app/microarray_signal.mp4`.

Your goal is to build a reproducible, pure-Bash pipeline that extracts the signal intensity over time for different regions of the array, computes the signal growth rate using linear regression, and serves the results via a simple HTTP API.

Step 1: Domain Decomposition & Signal Extraction
The flow cell consists of a 2x2 grid of sensors. However, the video is high-resolution. Using bash CLI tools (like `ffmpeg` and `imagemagick`, which are pre-installed), you must:
1. Extract every frame of the video.
2. Downsample/aggregate each frame into a 2x2 grayscale grid (representing the 4 microarray domains: coordinates `x,y` where x∈{0,1} and y∈{0,1}).
3. Extract the 8-bit grayscale pixel intensity (0-255) for each of the 4 domains across all frames.

Step 2: Curve Fitting (Linear Regression)
Using pure Bash (e.g., `awk`), perform a linear regression on the intensity values for each of the 4 domains over time.
- The independent variable `X` is the frame index (starting at X=1 for the first frame).
- The dependent variable `Y` is the grayscale intensity.
- Calculate the slope `m` of the best-fit line (Y = mX + b) for each of the 4 coordinates. Round the slope to 2 decimal places.

Step 3: Serve the Results
Write a bash script named `/home/user/serve_results.sh` that starts a continuously running HTTP service listening on `0.0.0.0:9090` (you may use `socat` or `nc`).
- The service must accept `GET` requests to the endpoint `/slope/<x>/<y>` (e.g., `/slope/0/1`).
- The service MUST require a custom authentication header: `X-Bio-Auth: secret-token-77`. If this header is missing or incorrect, return an `HTTP/1.1 401 Unauthorized` response.
- If the header is correct and the endpoint is valid, return an `HTTP/1.1 200 OK` response where the body contains ONLY the calculated slope (e.g., `5.00`) as plain text.

All data processing and the web server must be implemented using Bash scripts and standard CLI utilities. Do not use Python, Node, R, or other scripting languages. Run your server in the background once it is ready.
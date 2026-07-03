I'm a data engineer working on an ETL pipeline to analyze traffic camera footage, but I'm running into a few issues. I need you to build the pipeline, fix a visualization bug, and serve the results.

Here is what you need to do:

1. **Video Processing (ETL Pipeline)**
There is a video file located at `/app/video_sample.mp4`. Write a Python script (`/home/user/pipeline.py`) that extracts all frames from this video. For every pair of consecutive frames (frame `i` and frame `i-1`, starting with `i=1`), convert them to grayscale (by averaging the R, G, and B channels) and compute the Mean Squared Error (MSE) between the two matrices. 
Save these MSE values to a JSON file at `/home/user/mse_results.json` as a simple list of floats `[mse_1, mse_2, ...]`.

2. **Fix the Visualization Script**
I wrote a script at `/home/user/generate_plot.py` to plot these MSE values, but because we are running in a headless environment, it either crashes or produces a completely blank `motion_plot.png` file. Please debug and fix `/home/user/generate_plot.py` so that it successfully reads `/home/user/mse_results.json` and outputs a correct, non-blank line plot to `/home/user/motion_plot.png`. Ensure it doesn't try to open GUI windows.

3. **Serve the Results (Multi-Protocol)**
Create a service (`/home/user/server.py`) that runs in the background and exposes our ETL results via two protocols:
- **HTTP Service (Port 8080):** 
  Listen on `0.0.0.0:8080`. When a `GET` request is made to `/stats`, it should return a JSON response with the frame index that had the highest MSE, and the MSE value itself. Format: `{"max_mse_frame": <int>, "max_mse_value": <float>}`. (Note: `max_mse_frame` should be `i` from the frame pair `i` and `i-1`).
- **Raw TCP Service (Port 9090):**
  Listen on `0.0.0.0:9090`. When a TCP client connects and sends the exact string `"PLOT\n"`, the server must send back the raw binary contents of `/home/user/motion_plot.png` and then gracefully close the connection.

Please start the server in the background once everything is ready.
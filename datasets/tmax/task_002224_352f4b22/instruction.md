You are a performance engineer tasked with profiling the visual output of a complex scientific simulation to detect numerical instabilities. The simulation occasionally produces anomalous frames where the pixel intensity distribution deviates from the expected theoretical model due to floating-point errors. 

We have recorded a recent simulation run as a video, located at `/app/rendering.mp4`. 
The theoretically stable frame pixel intensities (in grayscale) are known to follow a scaled Beta distribution: `X ~ Beta(a=2.0, b=5.0) * 255`. 

Your objective is to build and run a Python web service that analyzes specific frames from the video on-demand to test for numerical stability.

Please accomplish the following:
1. **Environment Setup**: Set up your Python environment and install necessary scientific and web packages (e.g., `scipy`, `numpy`, `opencv-python-headless`, `fastapi`, `uvicorn`).
2. **Video Processing**: Extract the frames from `/app/rendering.mp4` so they can be processed. (You may use `ffmpeg` or OpenCV).
3. **Statistical Analysis Service**: Create a web server listening on `127.0.0.1` port `8080`.
4. **Endpoint Specification**: Implement a GET endpoint `/profile/{frame_index}`. When called, this endpoint should:
    - Load the specified frame (0-indexed) and convert it to grayscale.
    - Run a **Monte Carlo simulation** to generate exactly 100,000 samples from the theoretical stable distribution: `Beta(a=2.0, b=5.0) * 255`. Use a fixed random seed of `42` for this generation for reproducibility.
    - Calculate the **Wasserstein distance** (using `scipy.stats.wasserstein_distance`) between the flattened array of the frame's grayscale pixel intensities and the 100,000 Monte Carlo samples.
    - Perform a **Kolmogorov-Smirnov test** (`scipy.stats.ks_2samp`) comparing the flattened frame pixels against the 100,000 Monte Carlo samples.
    - Determine if the frame is numerically stable. A frame is considered `stable` (True) if the KS test `p-value > 0.01` AND the `wasserstein` distance is `< 10.0`. Otherwise, it is `False`.
    - Return a JSON response strictly in this format: 
      `{"frame": <int>, "wasserstein": <float>, "p_value": <float>, "stable": <bool>}`

Leave the web server running in the background or foreground so that our automated testing suite can query it via HTTP to verify your implementation. Make sure your server can handle multiple requests.
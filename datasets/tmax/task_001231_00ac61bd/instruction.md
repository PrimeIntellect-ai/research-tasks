You are acting as a data scientist analyzing the growth of a bacterial colony from a time-lapse video.

We have a video file located at `/app/bacteria_growth.mp4` recorded at 1 frame per second (each frame represents 1 hour of growth). Your task is to process this video, calculate the density of the bacterial colony over time, fit a mathematical model to the growth, and serve the results via a web API.

Please complete the following steps:

1. **Video Processing & Parallel Density Estimation**:
   - Extract the frames from `/app/bacteria_growth.mp4`.
   - Write a Bash script that uses parallel processing (e.g., GNU `parallel` or `xargs -P`) to analyze all frames efficiently.
   - For each frame, calculate the "bacterial density", defined strictly as the ratio of pixels with a grayscale intensity strictly greater than 128 to the total number of pixels in the frame. (Values should be between 0.0 and 1.0).

2. **Curve Fitting**:
   - The colony growth follows a standard logistic growth model: `D(t) = K / (1 + ((K - D0) / D0) * exp(-r * t))`
   - Where `D(t)` is the density at time `t` (frame index, starting at `t=0` for the first frame), `K` is the carrying capacity, `D0` is the initial density, and `r` is the growth rate.
   - Write a script (Python is acceptable) to fit this curve to your extracted density data and estimate the parameters `K`, `D0`, and `r`.

3. **API Service**:
   - Create a service (using Python, `nc`, etc.) listening on `127.0.0.1:8080`.
   - When it receives an HTTP GET request to the `/model` endpoint, it must respond with a `200 OK` status and a JSON payload containing the fitted parameters.
   - The JSON payload must exactly match this format:
     `{"K": <float>, "D0": <float>, "r": <float>}`
   - The service must remain running so it can be queried by our automated verification system.

Ensure your service handles standard HTTP GET requests and returns valid JSON. Keep the server running in the background.
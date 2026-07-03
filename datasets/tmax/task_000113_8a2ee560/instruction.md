You are an AI assistant helping a physics researcher analyze an experimental video of a falling mass. The researcher needs a fully automated Bash-based pipeline to process the video, extract kinematic data, perform numerical and statistical analysis, and serve the results via a web API.

The experiment video is located at `/app/drop_test.mp4`. The video features a single bright white circular mass falling against a pitch-black background.
- **Framerate:** 30 frames per second.
- **Scale:** 1 pixel = 0.005 meters.

Your task is to write a Bash-orchestrated workflow that performs the following steps:

1. **Frame Extraction & Tracking:**
   Use `ffmpeg` to extract the frames. Determine the vertical (Y) center of the mass in each frame (you may write a helper Python script using OpenCV/cv2 or standard image libraries, but the orchestration must be in Bash). Output this raw position data to `/home/user/trajectory.csv` (format: `frame_index, y_pixel`).

2. **Curve Fitting & Regression:**
   Fit the extracted Y-trajectory data to two models:
   - Linear: $y(t) = m t + c$ (constant velocity hypothesis)
   - Quadratic: $y(t) = a t^2 + b t + c$ (constant acceleration hypothesis)
   Calculate the Residual Sum of Squares (RSS) for both fits to statistically compare the hypotheses. 
   Extract the acceleration in $m/s^2$ from the quadratic fit (remember: $y = \frac{1}{2} g t^2 + v_0 t + y_0$, and convert pixels/frame^2 to $m/s^2$).

3. **Numerical Differentiation & Integration:**
   Using the raw position data, compute the numerical derivative (velocity in $m/s$) at each step using finite differences. Then, numerically integrate this velocity curve (e.g., using the trapezoidal rule) to compute the total displacement in meters.

4. **Service Integration:**
   Create and launch a web service (using Python, `nc`, or whatever you prefer, launched via Bash) listening on `0.0.0.0:9090`. 
   It must accept a `GET /analysis` request and respond with `200 OK` and a JSON payload exactly matching this structure:
   ```json
   {
     "acceleration_m_s2": <float>,
     "linear_rss": <float>,
     "quadratic_rss": <float>,
     "integrated_displacement_m": <float>
   }
   ```
   *Round all floats to 3 decimal places.*

Leave the server running in the background. Do not require any authentication. Ensure all dependencies (like `flask` or `opencv-python`) are installed via `pip` if you use them.
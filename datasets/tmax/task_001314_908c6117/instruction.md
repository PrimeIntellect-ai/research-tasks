You are a data scientist studying a rare bioluminescent organism. You have been provided with a video recording of the organism's light emissions over time. Your goal is to extract the temporal signal from the video, analyze its spectral properties to find the dominant pulsation frequency, and deploy a local API that can dynamically analyze specific frame ranges upon request.

**Part 1: Data Extraction and Analysis**
1. The video is located at `/app/flicker_experiment.mp4`. It was recorded at exactly 30 frames per second (FPS).
2. Extract the frames of the video. For each frame, convert it to grayscale and calculate the mean pixel intensity across the entire frame. This sequence of mean intensities forms your 1D time-series signal.
3. Perform a Fast Fourier Transform (FFT) on this time-series to identify the dominant frequency (in Hertz) of the organism's pulsation. 
4. Implement a statistical test to determine if this dominant frequency is statistically significant compared to the background noise. For this task, consider the signal "significant" if the amplitude of the dominant frequency (excluding the 0 Hz DC component) is strictly greater than 3.0 times the mean amplitude of all other non-zero frequencies in the spectrum.

**Part 2: API Deployment**
You must write and start an HTTP server (in the language of your choice) listening on `127.0.0.1:8080`. 
The server must expose a single endpoint:
- **Endpoint:** `/analyze`
- **Method:** `POST`
- **Content-Type:** `application/json`
- **Request Body format:** `{"start_frame": <int>, "end_frame": <int>}` (both inclusive, 0-indexed).
- **Processing:** When a request is received, the server should slice the extracted time-series signal to the specified frame range. It must then apply the FFT and significance test (as described in Part 1) *only* to that slice. Assume the 30 FPS rate remains constant.
- **Response Format:** A JSON object containing exactly two keys:
  - `"dominant_frequency_hz"`: The dominant frequency in Hz (float, rounded to 2 decimal places).
  - `"is_significant"`: A boolean (`true` or `false`) indicating if the dominant frequency's amplitude is > 3.0 times the mean of the rest of the spectrum for this slice.

Keep the server running in the background or foreground so that it can be tested. Ensure your server handles potential errors gracefully (e.g., if the frame range is invalid or too short to compute an FFT).

Let me know once your API is up and running!
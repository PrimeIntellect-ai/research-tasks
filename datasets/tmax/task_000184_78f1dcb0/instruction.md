You are a machine learning engineer preparing training data from an aeroelastic simulation. We have recorded the simulation output as a video, but we suspect the simulation has a non-reproducible floating-point reduction order bug in certain mesh sub-domains, leading to divergent vibration frequencies.

Your task is to build a mesh analysis HTTP service in Python that extracts dominant frequencies from the simulation video using Fourier Transforms, and acts as a regression test to identify divergent sub-domains.

Resources provided:
1. Simulation video: `/app/aero_mesh_sim.mp4` (Assume it is exactly 30 FPS).
2. Baseline regression data: `/app/baseline_freqs.json` (Contains expected dominant frequencies for specific mesh sub-domains).

You must write and run an HTTP server listening on `127.0.0.1:8080`. The server must implement a single endpoint:
- **POST `/analyze_mesh`**
- **Payload:** JSON object defining a mesh bounding box: `{"x_min": <int>, "y_min": <int>, "x_max": <int>, "y_max": <int>}`
- **Response:** JSON object: `{"dominant_frequency": <float>, "is_divergent": <bool>}`

To process a request:
1. Extract all frames from `/app/aero_mesh_sim.mp4` (you can use ffmpeg or OpenCV).
2. For each frame, compute the mean pixel intensity (grayscale) within the specified bounding box `[y_min:y_max, x_min:x_max]`.
3. This creates a time-domain signal. Apply a Fast Fourier Transform (FFT) to this signal.
4. Identify the dominant frequency (in Hz) corresponding to the peak magnitude in the FFT (excluding the DC component at 0 Hz).
5. Compare this frequency to the baseline. The baseline JSON is structured as `"x_min,y_min,x_max,y_max": expected_freq_float`. Look up the exact bounding box in `/app/baseline_freqs.json`.
6. If the absolute difference between your computed dominant frequency and the baseline frequency is greater than `0.05` Hz, mark `is_divergent` as `true`. Otherwise, `false`.

Start the service and leave it running in the background. Write a file `/home/user/service_ready.txt` when the server is up and listening. We will test it by sending HTTP POST requests.
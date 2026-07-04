You are an AI data scientist. We have recorded a physical experiment involving a vibrating mechanical component. The video is located at `/app/vibration.mp4` (recorded at 30 frames per second). We also have a baseline reference signal in `/app/reference_signal.csv` (contains a single column of position values).

Your task is to analyze this video, extract the signal, process it, and serve the results via a REST API.

**Step 1: Signal Extraction**
Extract the frames from `/app/vibration.mp4`. In each frame, locate the centroid (center of mass) of the brightest pixels (convert to grayscale, threshold at pixel value > 200). The x-coordinate of this centroid represents the displacement signal $x(t)$. 

**Step 2: Signal Processing & SSA**
1. Compute the velocity signal $v(t)$ using second-order accurate central numerical differentiation on $x(t)$. 
2. Perform Singular Spectrum Analysis (SSA) on $x(t)$ with a window length of 30. Form the trajectory matrix and perform SVD. Note: Because the signal is highly periodic, the trajectory matrix will be near-singular. Reconstruct the filtered signal $x_{filtered}(t)$ using only the top 2 principal components.

**Step 3: Spectral Analysis & Confidence Intervals**
1. Compute the Fast Fourier Transform (FFT) of $x_{filtered}(t)$ to find the dominant frequency (the frequency with the highest magnitude, excluding 0 Hz DC component).
2. Perform a Moving Block Bootstrap on $x_{filtered}(t)$ to find the 95% confidence interval for this dominant frequency. Use a block size of 15 frames and 500 bootstrap iterations. Calculate the 2.5th and 97.5th percentiles.

**Step 4: Reference Comparison**
Calculate the Mean Squared Error (MSE) between your $x_{filtered}(t)$ and the reference signal in `/app/reference_signal.csv` (assuming both start at frame 0).

**Step 5: API Service**
Create and run a Python web server (e.g., using Flask or FastAPI) listening on `127.0.0.1:8000`. It must implement the following endpoints:
- `GET /api/frequency`: Returns JSON `{"frequency": <float>, "ci_lower": <float>, "ci_upper": <float>}`.
- `GET /api/velocity?frame=<int>`: Returns JSON `{"velocity": <float>}` for the specified frame index (0-indexed).
- `GET /api/reference_diff`: Returns JSON `{"mse": <float>}`. This endpoint MUST require a Bearer token for authorization: `Bearer data-sci-token-882`. If the token is missing or invalid, return a 401 status code.

Leave the server running in the foreground or background so it can be queried by our automated test suite.
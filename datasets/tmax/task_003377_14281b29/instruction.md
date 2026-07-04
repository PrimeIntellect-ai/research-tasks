You are a data scientist analyzing spectral data from a chemical reaction. The raw sensor data is provided as a video file located at `/app/reaction_spectroscopy.mp4`. 

Your task is to extract the time-series spectral data from this video, factorize it into constituent chemical signatures using a custom Non-negative Matrix Factorization (NMF) implementation, and serve the results via an HTTP API.

Step 1: Data Extraction
1. Extract all frames from `/app/reaction_spectroscopy.mp4` using `ffmpeg` (e.g., as PNGs). The video frames are in grayscale.
2. Read the pixel intensities. For each frame (sorted in chronological order based on standard `ffmpeg` output frame numbering, e.g., `%04d.png`), extract exactly the 50th row (index 49, assuming 0-indexed) of the image as a 1D numpy array. 
3. Stack these 1D arrays vertically to form a matrix `V` of shape `(num_frames, width)`. Divide the matrix by 255.0 to normalize the values to the `[0, 1]` range.

Step 2: Matrix Factorization
Standard NMF solvers often fail with division-by-zero errors on our sensor data due to near-singular inputs (regions of absolute zero intensity). You must implement a custom NMF in Python using the Multiplicative Update rules with a small epsilon to prevent this.
1. We want to factorize `V` into `W` (shape `num_frames, k`) and `H` (shape `k, width`) where `k = 2` components.
2. Initialize both `W` and `H` as matrices filled with exactly the value `0.5`.
3. Perform exactly 100 iterations of the following multiplicative updates:
   First update H: 
   `H = H * (W.T @ V) / (W.T @ W @ H + 1e-9)`
   Then update W:
   `W = W * (V @ H.T) / (W @ H @ H.T + 1e-9)`
   (where `@` is matrix multiplication and `*` is element-wise multiplication).

Step 3: Serve the Results
Create a Python HTTP server (e.g., using Flask or FastAPI) that listens on `127.0.0.1:9090` and exposes the following endpoints:
- `GET /W`: Returns the `W` matrix as a JSON list of lists.
- `GET /H`: Returns the `H` matrix as a JSON list of lists.
- `GET /health`: Returns a JSON object `{"status": "ok"}`.

Ensure your server runs continuously in the background or foreground so that it can respond to verification requests. Do not use authentication. The server must be up and running as the final state of the task.
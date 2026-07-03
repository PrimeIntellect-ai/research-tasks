You are acting as a bioinformatics analyst analyzing fluorescent droplet-based sequencing data. We have captured a video of the sequencing flow cell, and we need to analyze the intensity distributions of the droplets over time to ensure the sequence reads are converging to our expected theoretical quality distribution. 

Your task involves several stages: environment setup, video processing, mathematical convergence testing, and finally, serving the results via multiple network protocols.

Here are your detailed instructions:

1. **Environment Setup & Scientific Code**
   - You have access to a video file at `/app/sequencing_droplets.mp4`.
   - Set up a Python virtual environment at `/home/user/venv` and install any necessary packages (e.g., `numpy`, `scipy`, `opencv-python`, `flask`).

2. **Video Processing & Distribution Extraction**
   - The video is in grayscale. For each frame (starting from index 1, i.e., 1, 2, 3... up to the end of the video), calculate the normalized histogram of pixel intensities (bins 0 to 255).
   - Let $H_i$ be the normalized histogram (an array of 256 probabilities summing to 1) for the $i$-th frame.
   - Let $A_N = \frac{1}{N} \sum_{i=1}^N H_i$ be the average normalized histogram of the first $N$ frames.

3. **Convergence Testing with Probability Distribution Distance**
   - We have provided a theoretical reference distribution in `/app/ref_dist.json`. This file contains a JSON list of 256 float values summing to 1.
   - For each $N \ge 1$, compute the 1st Wasserstein distance (Earth Mover's Distance) between $A_N$ and the reference distribution. Use `scipy.stats.wasserstein_distance` (treating the indices 0-255 as the values and the histogram arrays as the weights/probabilities).
   - Let $W_N$ be the Wasserstein distance for the first $N$ frames.
   - Find the **smallest** $N \ge 2$ such that the absolute difference $|W_N - W_{N-1}| < 10^{-4}$. This is your `converged_N`. 
   - Record the Wasserstein distance at this $N$ as `converged_W`.

4. **Multi-Protocol Service Integration**
   - We need to integrate your analysis into our automated pipeline by exposing the results over two distinct protocols simultaneously.
   - **Service 1 (HTTP API):** 
     - Write a Python script that runs a web server on `127.0.0.1:8080`.
     - Implement a `GET /convergence` endpoint that returns a JSON response in the exact format: `{"converged_N": <int>, "wasserstein_distance": <float>}`. The float should be rounded to 6 decimal places.
   - **Service 2 (TCP Socket):**
     - In the same script (using threading, async, or running a separate process), start a raw TCP server listening on `127.0.0.1:9090`.
     - Whenever a client connects and sends the exact string `PING\n`, the server must respond with `PONG <converged_N>\n` and then close the connection.

Ensure both services are running and listening indefinitely in the background before you declare the task complete. The automated testing suite will connect to both `127.0.0.1:8080` via HTTP and `127.0.0.1:9090` via raw TCP to verify your implementation.
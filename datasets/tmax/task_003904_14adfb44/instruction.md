You are acting as a Machine Learning Engineer preparing a synthetic and empirical training dataset for a physics-informed neural network. 

We have an experiment video of a vibrating mechanical oscillator located at `/app/experiment.mp4` (recorded at 60 FPS). We also have a parallelized Python simulation of this system located at `/home/user/sim_parallel.py`. 

Unfortunately, the parallel simulation currently produces non-reproducible results. Across multiple runs with the exact same seed, the final aggregated system energy fluctuates at the floating-point level (e.g., 1e-12 differences). This is ruining our downstream ML training which requires exact bit-for-bit reproducibility for regression testing.

Your task consists of four parts:

1. **Experimental Spectral Analysis:**
   - Extract the frames from `/app/experiment.mp4`.
   - In each frame, find the X-coordinate of the brightest pixel (representing our oscillator marker).
   - Perform a Fast Fourier Transform (FFT) on the resulting X-coordinate time series to find the dominant frequency (the frequency with the highest magnitude, excluding the 0 Hz DC component).
   - Generate a plot of the frequency spectrum and save it to `/home/user/spectrum.png`.

2. **Numerical Stability & Reproducibility:**
   - Inspect and fix `/home/user/sim_parallel.py`. 
   - The script uses `multiprocessing` to run Monte Carlo samples of the oscillator's energy and sums them. The non-reproducibility is caused by a floating-point reduction order issue (the processes return results asynchronously, and they are added to a running total in completion order).
   - Fix the script so that the Monte Carlo results are aggregated in a strictly deterministic order (e.g., sorted by their sample index before summing), ensuring bit-for-bit reproducible output across multiple runs.
   - The fixed script should output the exact same floating-point value every time it is run.

3. **Service Integration:**
   - Create and start a Python HTTP API (using Flask or FastAPI) listening on `127.0.0.1:8080`.
   - The API must implement the following endpoints:
     - `GET /frequency`: Returns a JSON object `{"video_dominant_hz": <float>}` containing the dominant frequency you calculated in Part 1.
     - `POST /simulate`: Runs your fixed `sim_parallel.py` simulation internally, and returns a JSON object `{"energy": <float>}` containing the reproducible aggregated energy value.

4. **Background Execution:**
   - Keep the HTTP server running in the background so it can be queried by our automated verification suite.

Ensure your code handles paths correctly and that the API precisely matches the required JSON schemas.
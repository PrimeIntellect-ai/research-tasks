You are an AI assistant acting as a bioinformatics analyst. You have been given a dataset consisting of a biological assay video and a FASTA file. 

Your objective is to extract experimental data from the video, perform statistical and numerical analysis, parse the sequence data, generate a visualization, and serve the results via an HTTP API.

**Task Steps:**
1. **Video Processing:**
   - A video file is located at `/app/assay_video.mp4`. It contains 50 frames (numbered 0 to 49).
   - Use `ffmpeg` or Python (e.g., OpenCV) to extract the frames.
   - For each frame, convert it to grayscale. Calculate the mean intensity of the center 100x100 pixel region. The video resolution is 400x400, so the center region is from x=150 to 250, and y=150 to 250.
   - Let $I(t)$ be the mean intensity at frame $t$.

2. **Nonlinear Equation Solving:**
   - The intensity follows Michaelis-Menten-like kinetics over time: $I(t) = \frac{V_{max} \cdot t}{K_m + t}$.
   - Fit this nonlinear equation to your extracted data $(t, I(t))$ for $t \in \{0, 1, ..., 49\}$ to solve for the parameters $V_{max}$ and $K_m$. 

3. **Probability Distribution Distance:**
   - Extract the flat arrays of the 100x100 pixel grayscale values from the *first frame* (t=0) and the *final frame* (t=49).
   - Calculate the 1D Wasserstein distance between these two pixel intensity distributions. Use `scipy.stats.wasserstein_distance`.

4. **Bioinformatics Parsing:**
   - Parse the file `/app/targets.fasta`.
   - For each sequence, calculate the GC content (percentage of G and C bases, represented as a float between 0.0 and 100.0).

5. **Visualization:**
   - Create a plot showing the raw extracted intensities as a scatter plot, and the fitted curve as a line. Save this plot to `/home/user/assay_fit.png`.

6. **Network Service (multi_protocol):**
   - Write a Python HTTP server (e.g., using Flask or FastAPI) listening on `127.0.0.1:8000`.
   - Implement the following endpoints:
     - `GET /kinetics` : Returns JSON `{"V_max": float, "K_m": float}` rounded to 4 decimal places.
     - `GET /distance` : Returns JSON `{"wasserstein_distance": float}` rounded to 4 decimal places.
     - `GET /gc_content` : Returns JSON `{"sequence_id": float}` mapping each FASTA header ID (without the `>`) to its GC content percentage, rounded to 2 decimal places.

Run the server in the background so it is available for automated verification. Keep it running.
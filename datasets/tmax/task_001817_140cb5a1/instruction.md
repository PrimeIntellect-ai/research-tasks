I am a researcher studying the vibrational dynamics of a molecular spring-mass network. I have a video recording of the simulation run located at `/app/membrane_vib.mp4`. The video captures the fluorescence intensity of the network over time, sampled at 60 FPS. 

However, my analysis pipeline broke down. I need you to write a comprehensive Bash script (`/home/user/analyze_dynamics.sh`) that orchestrates the following tasks using CLI tools (you may use inline Python/R/Awk where appropriate, but the primary pipeline must be driven by Bash):

1. **Signal Extraction**: Extract all frames from `/app/membrane_vib.mp4`. Calculate the average grayscale intensity of the central 100x100 pixel region (bounding box: x=270 to 370, y=190 to 290, assuming a 640x480 video) for each frame. Output this time series to `/home/user/intensity_signal.txt`.
2. **Spectral Analysis**: Compute the discrete Fourier transform (FFT) of the zero-meaned intensity signal to find the dominant resonant frequency (in Hz). 
3. **Statistical Bootstrapping**: Implement a block bootstrap (block size = 30 frames, 1000 resamples) on the time series. For each resample, compute the dominant frequency. Use this to determine the 95% confidence interval (using the percentile method) for the dominant frequency.
4. **Network Topology Fix**: I also have the network's Laplacian matrix in `/app/laplacian.csv`. I was trying to compute the effective resistance matrix, but the pseudo-inverse fails because the matrix is near-singular and poorly conditioned due to a floating-point truncation artifact. Write a step in your script that reads `laplacian.csv`, regularizes it by adding a small Tikhonov term (0.01) to the diagonal, computes the inverse, and finds the trace of this inverse matrix.
5. **Output**: Combine all your findings into a single JSON file at `/home/user/results.json` with the following schema:
```json
{
  "dominant_frequency_hz": <float>,
  "ci_95_lower": <float>,
  "ci_95_upper": <float>,
  "regularized_inverse_trace": <float>
}
```

The script `/home/user/analyze_dynamics.sh` must be executable and automatically perform all these steps from start to finish. I will run the script, and I expect `/home/user/results.json` to be generated with accurate values.
You are an astrophysical researcher analyzing a simulation video of a 1D fluctuating light source. You need to extract the signal, find its periodic properties, run a Monte Carlo simulation of its behavior, and measure how well your simulation matches the original data. 

You must accomplish this using ONLY Bash, awk, and standard coreutils (no Python, R, or compiled C/C++ unless you write it as a quick script). `ffmpeg` is available for video processing.

Here are your steps:
1. **Signal Extraction:** The video file is located at `/app/pulsar.mp4`. Extract the average grayscale brightness (luma/Y component) for every frame in the video sequentially.
2. **Spectral Analysis (DFT):** Write an `awk` script to compute the Discrete Fourier Transform (Power Spectrum) of the mean brightness time series. Identify the dominant non-DC frequency bin $k$ (where frequency $f = k/N$, $N$ being the number of frames).
3. **Monte Carlo Simulation:** Write a Bash/awk script to simulate 100,000 samples of the system's expected brightness. The system model is: 
   $S_t = \mu + A \cos(2\pi f t + \phi) + \epsilon$
   Where:
   - $\mu$ is the mean brightness of the empirical video frames.
   - $f$ is the dominant frequency found in step 2.
   - $A$ is the amplitude of the dominant frequency.
   - $\phi$ is the phase (you can estimate it, or assume 0 for the amplitude distribution).
   - $\epsilon$ is uniform random noise strictly between -5.0 and +5.0.
   - $t$ is drawn uniformly at random from $[0, N]$.
4. **Distribution Distance:** Bin both the empirical brightness data (from the video frames) and your simulated Monte Carlo data into 10 equally sized bins spanning the minimum to the maximum empirical brightness. 
5. Calculate the Total Variation Distance (TVD) between the two probability distributions.
6. Write the simulated probability distribution (the 10 fractional frequencies, one per line) to `/home/user/sim_dist.txt`. 
7. Write a short report to `/home/user/report.txt` containing the dominant frequency, TVD, and summary statistics.

To succeed, your Monte Carlo output distribution in `/home/user/sim_dist.txt` must closely match the theoretical simulated distribution, ensuring the Mean Absolute Error (MAE) between your bin probabilities and the true model bin probabilities is less than 0.05.
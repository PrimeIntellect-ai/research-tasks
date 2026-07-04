As a bioinformatics analyst, your objective is to analyze a simulated fluorescence microscopy video of molecular sequence tags and estimate their diffusion parameters using MCMC, finally serving the statistical results via a custom HTTP server written in C.

Your tasks are:
1. Extract frames from the video fixture located at `/app/fluor_seq.mp4` using `ffmpeg` (which is pre-installed). The video has exactly 50 frames.
2. Write a C program that processes these frames (you may convert them to raw grayscale or PGM format via `ffmpeg` first) to identify the single brightest pixel in each frame, representing our molecular tag.
3. Build a simple tracking graph that calculates the squared displacement ($\Delta r^2 = \Delta x^2 + \Delta y^2$) of the tag between consecutive frames ($\Delta t = 1$).
4. Implement a Metropolis-Hastings MCMC sampler in C to estimate the posterior distribution of the diffusion coefficient $D$. Assume the likelihood of each displacement follows a 2D random walk: $P(\Delta r | D) \propto \frac{1}{D} \exp(-\frac{\Delta r^2}{4D})$. Use a uniform prior for $D \in [0.1, 100.0]$. Run the sampler for 100,000 iterations (discarding the first 10,000 as burn-in) to calculate the posterior mean and standard deviation of $D$.
5. Implement an HTTP server in C (using raw sockets or a lightweight library if available, but raw POSIX sockets are preferred for zero-dependency) that listens on `127.0.0.1:8080`.
6. When your server receives a `GET /posterior` HTTP request, it must respond with a `200 OK` status and a JSON payload containing the MCMC results in exactly this format:
   `{"mean_D": 12.34, "std_D": 1.23}`
   (Format values to 2 decimal places).

Ensure the server stays running in the background so it can be queried by the automated verification suite.
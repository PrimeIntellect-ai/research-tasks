You are helping a physics researcher analyze an experiment involving anomalous diffusion. We have a video of a fluorescent particle moving in a viscoelastic medium, and we need to extract its trajectory, estimate the parameters of its motion using a parallelized MCMC approach, and finally serve the simulation results via a web API.

Here are the specific steps you need to follow:

1. **Video Analysis**:
   - There is a video of the experiment located at `/app/experiment.mp4`. 
   - Extract the frames and track the coordinates of the single bright particle in the video. The video is 30 FPS, and the particle is the brightest spot in each frame.
   - Save the extracted $(x, y)$ coordinates in a CSV file at `/home/user/trajectory.csv` with columns `frame,x,y`.

2. **MCMC Parameter Estimation (C++)**:
   - The particle's motion is modeled by a Fractional Brownian Motion (fBM) with parameters $D$ (generalized diffusion coefficient) and $\alpha$ (anomalous exponent).
   - Write a C++ program at `/home/user/mcmc_sampler.cpp` that implements a Markov Chain Monte Carlo (MCMC) sampler (e.g., Metropolis-Hastings) to estimate $D$ and $\alpha$ from the `trajectory.csv` data.
   - The sampler must use **OpenMP** to parallelize the likelihood computation or run multiple parallel chains.
   - The estimated posterior means should be saved to `/home/user/parameters.txt` in the format: `D=<value>\nalpha=<value>`.

3. **Simulation Service**:
   - Create a web service listening on `localhost:8080`. You may write this in Python (e.g., using Flask or FastAPI) which calls your compiled C++ binary, or natively in C++.
   - The service must implement an HTTP GET endpoint `/simulate?steps=<N>` which returns a JSON response containing a newly simulated trajectory (using the estimated mean $D$ and $\alpha$) with `<N>` steps.
   - The JSON response format must be: `{"trajectory": [{"x": float, "y": float}, ...]}` starting from `x=0, y=0`.
   - Leave the server running in the background.

Please complete the implementation, compile the C++ code with `-fopenmp`, run the pipeline, and start the service on port 8080.
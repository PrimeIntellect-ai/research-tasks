You are acting as a bioinformatics systems analyst. We are analyzing a time-series fluorescence microscopy video of a cellular biosensor reacting to a chemical stimulus. The video is located at `/app/fluorescence.mp4`.

Your task requires extracting data from this video, fitting a biophysical decay model using Bayesian inference (MCMC) in C, storing the results in a scientific data format, and exposing the analysis via an internal API.

Here are the exact requirements:

1. **Video Processing**:
   Extract the mean pixel intensity of each frame from `/app/fluorescence.mp4` (which is a grayscale video at 10 frames per second). Let $t$ be the time in seconds (where frame 0 is $t=0.0$, frame 1 is $t=0.1$, etc.), and $I(t)$ be the mean pixel intensity.

2. **C Mathematical Modeling & I/O**:
   Write a C program (e.g., `fit_decay.c`) that:
   - Takes the extracted $(t, I(t))$ data.
   - Fits the nonlinear biophysical model: $I(t) = A \cdot \exp(-B \cdot t) + C$
   - Uses a Metropolis-Hastings MCMC algorithm to sample the posterior distribution of the parameters $A$, $B$, and $C$.
     - Assume uniform priors for $A \in [0, 255]$, $B \in [0, 10]$, $C \in [0, 255]$.
     - Assume a Gaussian likelihood with a fixed standard deviation $\sigma = 2.0$.
     - Run the MCMC chain for exactly 10,000 iterations.
   - Writes the resulting MCMC chain to an HDF5 file named `/home/user/posterior.h5`. The file must contain a single dataset named `mcmc_chain` of shape `(10000, 3)` (with columns representing $A$, $B$, and $C$, in double precision).
   - You may install any necessary C libraries (e.g., `libhdf5-dev`).

3. **Analysis Service (Multi-protocol)**:
   Create and run an HTTP service listening on `0.0.0.0:8080`. You may write this service in Python or C.
   - It must expose a `GET /api/v1/posterior_means` endpoint.
   - The endpoint must be protected by an authentication header: `X-API-Key: bio-secret-994`. Requests without this exact header should return an HTTP 401 Unauthorized status.
   - When a valid request is received, the service should read `/home/user/posterior.h5`, discard the first 5,000 samples as burn-in, compute the mean of $A$, $B$, and $C$ over the remaining 5,000 samples, and return a JSON response exactly like:
     `{"A": <mean_A>, "B": <mean_B>, "C": <mean_C>}`

Ensure your HTTP server remains running in the background or foreground so that the verification tests can query it.
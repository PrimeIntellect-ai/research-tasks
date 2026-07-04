You are a performance engineer profiling a newly developed numerical integrator for physics simulations. The integrator has been failing due to a bug in its step-size adaptation logic, causing it to diverge wildly after a certain point. 

A diagnostic tool has captured the integrator's step-size behavior and exported it as a video artifact located at `/app/integrator_profile.mp4`. In this video, each frame represents a simulation step. The background is completely black, and a single red dot (pure RGB: `255, 0, 0`) tracks the simulation state. The `x` coordinate of the dot corresponds to the frame number (progress), and the `y` coordinate represents the integration step size.

Your task is to analyze this video, model the divergence, and serve the results via an API for our automated monitoring system.

Follow these exact steps:
1. **Observational Data Reshaping**: Extract the frames from `/app/integrator_profile.mp4`. Analyze each frame to find the exact `y` coordinate of the red dot. Compile a time-series dataset of the `y` coordinate per frame.
2. **Phase Splitting**: The video has exactly 100 frames (0 to 99). Split your extracted `y` coordinates into "Phase 1" (frames 0 to 49) and "Phase 2" (frames 50 to 99). 
3. **Probability Distribution Distance**: Calculate the 1st Wasserstein distance (Earth Mover's Distance) between the empirical 1D distribution of Phase 1 `y` values and Phase 2 `y` values. 
4. **MCMC Posterior Estimation**: We suspect Phase 2 behaves like a noisy Gaussian process. Write a Metropolis-Hastings MCMC sampler from scratch (or use a standard library) to estimate the posterior mean and standard deviation of the Phase 2 `y` values. Assume a Normal likelihood function and uniform priors (Mean prior: `U(0, 480)`, Std Dev prior: `U(0.1, 200)`). Run your MCMC chain for at least 10,000 steps, discarding the first 1,000 as burn-in. Calculate the expected value (mean) of the posterior distribution for both the mean parameter and the standard deviation parameter.
5. **API Integration**: Create and start an HTTP server listening on `0.0.0.0:8888`. 
   - The server must expose a `GET /analysis` endpoint.
   - It must require an Authorization header exactly matching: `Authorization: Bearer perf-agent-secret`
   - If authorized, it must return a JSON response with exactly these keys:
     ```json
     {
       "wasserstein": <float>,
       "posterior_mean": <float>,
       "posterior_std": <float>
     }
     ```
   - Keep the server running in the background or foreground so the verifier can query it.

Ensure your API is robust and correctly handles the required authentication header.